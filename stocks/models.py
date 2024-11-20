from django.db import models, IntegrityError


# Create your models here.

class Stock(models.Model):
    class StockColor(models.TextChoices):
        SAMSUNG_E = ("#A6F7E2","삼성전자")
        SK = ("#B79BFF","SK하이닉스")
        LG = ("#FFE5A5","LG에너지솔루션")
        SAMSUNG_B = ("#C7FFA5","삼성바이오로직스")
        HYUNDAI = ("#F8A5FF","현대차")

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    color = models.CharField(max_length=50,choices=StockColor.choices, default=StockColor.SAMSUNG_E)
    is_domestic = models.BooleanField()

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.pk:
            last_object = Stock.objects.last()
            if last_object:
                last_pk = last_object.pk
                self.pk = last_pk + 1
                super().save(*args,**kwargs)
            else:
                super().save(*args,**kwargs)
        else:
            super().save(*args,**kwargs)

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