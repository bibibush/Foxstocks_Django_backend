from django.core.management import BaseCommand
import pandas as pd

from stocks.models import Stock


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            df = pd.read_csv("csv/stocks_stock.csv", encoding="cp949")
            df = df.drop("id",axis=1)
            records = df.to_dict(orient="records")
            updated_records = [{**record, "code":"0" * (6 - len(str(record["code"]))) + str(record["code"])} for record in records]
            stock_instances = [Stock(**record) for record in updated_records]
            Stock.objects.bulk_create(stock_instances, ignore_conflicts=True)
            print("success")
        except Exception as e:
            print(e)