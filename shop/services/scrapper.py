import re
import logging
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock
from typing import Any

import requests
from anyascii import anyascii
from django.utils.text import slugify
from django.db import transaction
from selectolax.parser import HTMLParser

from shop.models import Category, Product, Color, Brand, Image


lock = Lock()
logger = logging.getLogger(__name__)


def upload_brand_logo_to_local_media(logo: str, brand: Brand) -> None:
    with requests.Session() as session:
        response = session.get(logo)
        assert response.status_code == HTTPStatus.OK, 'Wrong status code'

    file_name = f'images/brand/{slugify(anyascii(brand.name))}.jpg'
    with open(f'media/{file_name}', 'wb') as file:
        file.write(response.content)

    brand.logo = file_name
    brand.save()


def upload_images_to_local_media(images: list[str], product: Product) -> None:
    for i, image in enumerate(images, start=1):
        with requests.Session() as session:
            response = session.get(image)
            assert response.status_code == HTTPStatus.OK, 'Wrong status code'

        with open(f'media/images/product/{product.slug}-{i}.jpg', 'wb') as file:
            file.write(response.content)

        Image.objects.create(
            product=product,
            image=f'images/product/{product.slug}-{i}.jpg',
            url=image,
        )


@transaction.atomic
def write_to_db(data: dict) -> None:
    brand = None
    if data['Brand']:
        brand, _ = Brand.objects.get_or_create(
            name=data['Brand'],
            defaults={
                'logo': data['Brand logo'],
            }
        )
        if brand and brand.logo:
            upload_brand_logo_to_local_media(data['Brand logo'], brand)

    product, _ = Product.objects.get_or_create(
        slug=f"{slugify(anyascii(data['Title']))}-{data['Url'].split('/')[-1]}",
        defaults={
            'title': data['Title'],
            'description': data['Description'][0] if data['Description'] else None,
            'price': data['Price'],
            'old_price': data['Old price'],
            'discount': data['Discount'],
            'source_url': data['Url'],
            'brand': brand,
        }
    )
    for category in data['Categories']:
        category, _ = Category.objects.get_or_create(
            slug=slugify(anyascii(category)),
            defaults={
                'name': category,
            }
        )
        product.categories.add(category)

    if data['Colors']:
        for color in data['Colors']:
            color, _ = Color.objects.get_or_create(
                name=color,
            )
            product.colors.add(color)

    if data['Images']:
        upload_images_to_local_media(data['Images'], product)

    logger.warning('Product %s saved', product.slug)


def clear_price(price: str) -> int | None:
    if not price:
        return None
    return int(re.sub(r'\D', '', price))


def parse_products(html_string: str, url: str) -> dict[str, Any]:
    tree = HTMLParser(html_string)
    categories = tree.css('#BreadcrumbsList a')
    categories = [c.text(strip=True) for c in categories[1:]]
    title = tree.css('h1 span')
    title = ' '.join([t.text(strip=True) for t in title])
    price = tree.css_first('.ProductCard__priceSale__qUu34')
    if price:
        price = clear_price(price.text(strip=True))
    else:
        price = tree.css_first('.ProductCard__priceRegular__sFepg')
        price = clear_price(price.text(strip=True))
    old_price = tree.css_first('.ProductCard__priceRegularWithSale__jhCPs')
    if old_price:
        old_price = clear_price(old_price.text(strip=True))
    else:
        old_price = None
    discount = None
    if old_price:
        discount = round((price / old_price) * 100 - 100, 2)

    colors = tree.css('.ColorPicker__colors__q-7EP a')
    if colors:
        colors = [c.attributes['title'].strip() for c in colors]
    else:
        colors = None
    sizes = tree.css('span.BaseSelectItem__selectItemLabel__usttW')
    if sizes:
        sizes = [s.text(strip=True) for s in sizes]
    else:
        sizes = None
    description = tree.css('.Accordion__accordionDescription__CckLI')
    if description and len(description) > 0:
        description = [d.text(strip=True) for d in description[:1]]
    else:
        description = None
    images = tree.css('.slick-slide img')
    if images:
        images = {i.attributes['src'] for i in images if
                  i.attributes['src'].startswith('https')}
    else:
        images = None
    brand = tree.css_first('figure a img')
    if brand:
        brand = brand.attributes['alt']
    else:
        brand = None

    brand_logo = tree.css_first('figure a img')
    if brand_logo:
        brand_logo = brand_logo.attributes['src']
    else:
        brand_logo = None
    return {
        'Title': title,
        'Description': description,
        'Price': price,
        'Old price': old_price,
        'Discount': discount,
        'Images': images,
        'Url': url,
        'Brand': brand,
        'Brand logo': brand_logo,
        'Categories': categories,
        'Colors': colors,
        'Sizes': sizes,
    }


def worker(qu: Queue, session: requests.Session) -> None:
    while not qu.empty():
        url = qu.get()
        logger.info('Working on %s, queue size=%s', url, qu.qsize())
        try:
            response = session.get(url=url, timeout=10)
            assert response.status_code == HTTPStatus.OK, 'Wrong status code'
            data = parse_products(response.text, url)
            with lock:
                write_to_db(data)
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects,
                requests.exceptions.RequestException,
                AssertionError,
        ) as error:
            logger.warning('%s, url %s', error, url)
            qu.put(url)
        except Exception as error:
            logger.exception('Url %s %s', url, error)


def get_product_links_from_sitemap(url: str) -> list[str]:
    with requests.Session() as session:
        response = session.get(url=url)
        assert response.status_code == HTTPStatus.OK, 'Wrong status code'

    tree = HTMLParser(response.text)
    loc = tree.css('loc')

    return [elem.text(strip=True)
            for elem in loc
            if elem.text(strip=True).startswith('https://answear.ua/p')]


def main():
    site_map_url = 'https://answear.ua/sitemap_product_00001.xml'
    product_links = get_product_links_from_sitemap(site_map_url)

    logger.info('Number of products found %s', len(product_links))

    session = requests.Session()
    queue = Queue()
    for link in product_links[5000: 5100]:
        queue.put(link)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(10):
            executor.submit(worker, queue, session)


if __name__ == '__main__':
    main()
