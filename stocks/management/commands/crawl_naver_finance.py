from django.core.management import BaseCommand

from stocks.crawling import NaverFinanceClass
from stocks.models import Stock


class Command(BaseCommand):
    def handle(self, *args, **options):
        codes = [query.code for query in Stock.objects.all()]
        crawling = NaverFinanceClass(codes)