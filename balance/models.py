from django.conf import settings
from django.db import models

# Create your models here.

class Invested(models.Model):
    input = models.PositiveBigIntegerField()
    company = models.ForeignKey("stocks.Stock",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user","company"],name="accounts_invested_uniq")
        ]