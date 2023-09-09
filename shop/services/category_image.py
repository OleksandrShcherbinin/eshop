import logging
from http import HTTPStatus
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

import requests
from selectolax.parser import HTMLParser

from shop.models import Category


logger = logging.getLogger(__name__)

TIME_OUT = 10


def worker(queue: Queue):
    while True:
        url, category = queue.get()
        logger.info('[WORKING ON] %s', url)
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )

                if response.status_code == HTTPStatus.NOT_FOUND:
                    logger.warning('Page not found %s', url)
                    break

                assert response.status_code in (
                    HTTPStatus.OK,
                    HTTPStatus.PERMANENT_REDIRECT,
                    HTTPStatus.PERMANENT_REDIRECT
                ), 'Bad response'

            tree = HTMLParser(response.text)

            images = [image for image in tree.css('a div img')]
            if images:
                image_url = images[0].attributes['src']
                logger.info('Downloading image from %s', image_url)
                with requests.Session() as session:
                    img_response = session.get(image_url, timeout=TIME_OUT)
                image_name = f'{category.name}.jpg'
                with open(f'media/images/category/{image_name}', 'wb') as file:
                    file.write(img_response.content)

                category.image = f'images/category/{image_name}'
                category.save()
                logger.info('DONE!!!')

        except (
            requests.Timeout,
            requests.TooManyRedirects,
            requests.ConnectionError,
            requests.RequestException,
            requests.ConnectTimeout,
            AssertionError
        ) as error:
            logger.exception('An error happen %s', error)
            queue.put(url)

        if queue.qsize() == 0:
            break


def main():
    categories = Category.objects.exclude(name='all')

    queue = Queue()
    url = 'https://www.google.com/search?um=1&hl=entbs=isz:l' \
          '&safe=active&nfpr=1&q={name}&start=1&tbm=isch'
    for category in categories:
        name = category.name
        if category.name == 'Він':
            name = 'Чоловічий'
        elif category.name == 'Вона':
            name = 'Жіночий'
        queue.put((url.format(name=f'{name} одяг'), category))

    worker_number = 5

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()
