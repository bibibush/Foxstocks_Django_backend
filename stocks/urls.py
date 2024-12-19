from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stocks.views import StockViewSet, StockListView, ChartDataAPIView, DataTableAPIView

app_name = "stocks"

router = DefaultRouter()
router.register(r"viewset",StockViewSet)

urlpatterns = [
    path("",include(router.urls)),
    path("list/",StockListView.as_view()),
    path("charts/",ChartDataAPIView.as_view()),
    path("table/",DataTableAPIView.as_view())
]