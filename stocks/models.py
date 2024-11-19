from django.db import models

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    is_domestic = models.BooleanField()