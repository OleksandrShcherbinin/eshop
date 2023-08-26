from time import perf_counter

from django.core.management.base import BaseCommand, CommandError

from shop.services.scrapper import main


class Command(BaseCommand):
    help = 'Scrape data from site'

    def handle(self, *args, **options):
        try:
            t1 = perf_counter()
            main()
            print(f'Time: {perf_counter() - t1:.2f} seconds')
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(self.style.SUCCESS('Successfully scraped data'))
