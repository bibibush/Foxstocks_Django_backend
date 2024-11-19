from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from stocks.crawling import NaverFinanceClass
from stocks.models import Stock
from stocks.serializers import StockSerializer


# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,format=None):
        stocks = Stock.objects.all()
        crawling = NaverFinanceClass()

        prices =[crawling.crawl(stock) for stock in stocks]
        stocks_dics = [dict(vars(stock)) for stock in stocks]
        for stock in stocks_dics:
            del stock["_state"]

        stock_data = [{**stock,"price":prices[index]} for index, stock in enumerate(stocks_dics)]
        return Response(stock_data)