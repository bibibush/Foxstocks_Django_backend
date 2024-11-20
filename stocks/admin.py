from django.contrib import admin

from stocks.models import Stock, DomesticStock


# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_filter = ("is_domestic",)
    actions = ["select_proper_color"]

    def select_proper_color(self,request,queryset):
        color_choices = {choice[1]: choice[0] for choice in Stock.StockColor.choices}
        for query in queryset:
            name = query.name
            query.color = color_choices[name]

        Stock.objects.bulk_update(queryset,fields=("color",))



@admin.register(DomesticStock)
class DomesticStockAdmin(admin.ModelAdmin):
    pass