from django.contrib import admin

from balance.models import Invested


# Register your models here.

@admin.register(Invested)
class InvestedAdmin(admin.ModelAdmin):
    pass