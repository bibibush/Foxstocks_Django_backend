from django.conf import settings
from django.db import models

# Create your models here.

class Invested(models.Model):
    input = models.PositiveIntegerField()
    initial_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField()
    company = models.ForeignKey("stocks.Stock",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user","company"],name="accounts_invested_uniq")
        ]
    def __str__(self):
        return f"{self.user.username} - {self.company}"