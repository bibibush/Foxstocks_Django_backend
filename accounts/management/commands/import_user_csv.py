from django.core.management import BaseCommand
import pandas as pd
from accounts.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            df = pd.read_csv("csv/accounts_user.csv", encoding="cp949")
            df = df.drop(["last_login","id"],axis=1)
            if "date_joined" in df.columns:
                df["date_joined"] = pd.to_datetime(df["date_joined"])

            records = df.to_dict(orient="records")
            user_instances = [User(**record) for record in records]
            for instance in user_instances:
                print(instance.date_joined)
                print(type(instance.date_joined))
            User.objects.bulk_create(user_instances, ignore_conflicts=True)
            print("success")
        except Exception as e:
            print(e)