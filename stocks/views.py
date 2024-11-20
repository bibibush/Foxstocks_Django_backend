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

        serializer = StockSerializer(stocks, many=True)
        prices =[crawling.crawl(stock) for stock in stocks]

        stock_data = [{**stock,"price":prices[index]} for index, stock in enumerate(serializer.data)]
        return Response(stock_data)