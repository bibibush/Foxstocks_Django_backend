from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("email address"),unique=True)
    invested = models.ForeignKey("Invested",on_delete=models.CASCADE,null=True,blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

class Invested(models.Model):
    total = models.PositiveBigIntegerField()
    company = models.ForeignKey("stocks.Stock",on_delete=models.CASCADE)

    def __str__(self):
        return self.total