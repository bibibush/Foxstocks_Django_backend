from django.shortcuts import render
from rest_framework import viewsets

from stocks.models import Stock
from stocks.serializers import StockSerializer


# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer