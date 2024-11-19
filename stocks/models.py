from django.db import models

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    is_domestic = models.BooleanField()

    def __str__(self):
        return self.name

class DomesticStockManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_domestic=True)

class DomesticStock(Stock):
    objects = DomesticStockManager()

    class Meta:
        proxy = True

    def save(self,*args,**kwargs):
        self.is_domestic = True
        super().save(*args,**kwargs)