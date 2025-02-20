from django.core.management import BaseCommand

from stocks.crawling import NaverFinanceClass
from stocks.models import Stock


class Command(BaseCommand):
    def handle(self, *args, **options):
        queries = Stock.objects.all()
        crawling = NaverFinanceClass()

        for query in queries:
            crawling.crawl(query)