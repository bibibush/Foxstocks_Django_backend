from django.contrib import admin

from stocks.models import Stock, DomesticStock


# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_filter = ("is_domestic",)

@admin.register(DomesticStock)
class DomesticStockAdmin(admin.ModelAdmin):
    pass