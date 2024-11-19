from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stocks.views import StockViewSet

app_name = "stocks"

router = DefaultRouter()
router.register(r"",StockViewSet)

urlpatterns = [
    path("",include(router.urls))
]