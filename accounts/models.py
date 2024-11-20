from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

    def save(self,*args,**kwargs):
        if not self.pk:
            last_user = User.objects.last()
            if last_user:
                last_pk = last_user.pk
                self.pk = last_pk + 1
                super().save(*args,**kwargs)
            else:
                super().save(*args,**kwargs)
        else:
            super().save(*args,**kwargs)