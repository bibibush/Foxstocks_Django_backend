from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from balance.models import Invested
from balance.serializers import InvestedSerializer
from stocks.ChartDatas import dayData, monthData, yearData, weekData
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
        user_id = request.GET.get("user_id")
        invests = Invested.objects.filter(user__id= user_id)

        stocks = Stock.objects.all()
        crawling = NaverFinanceClass()

        serializer = StockSerializer(stocks, many=True)

        if invests.exists():
            additional_data = []
            updated_invests= []
            for stock in stocks:
                crawled_data = crawling.crawl(stock)
                invest = invests.filter(company=stock).first()
                if invest:
                    invest.current_price = int(crawled_data["price"].replace(",",""))
                    updated_invests.append(invest)

                additional_data.append(crawled_data)

            Invested.objects.bulk_update(updated_invests,["current_price"])
            invests_serializer = InvestedSerializer(updated_invests,many=True)
            stock_data = [{**stock, **additional_data[index]} for index, stock in enumerate(serializer.data)]
            response_data = {"data":stock_data,"invests":invests_serializer.data}
        else:
            additional_data = [crawling.crawl(stock) for stock in stocks]
            stock_data = [{**stock, **additional_data[index]} for index, stock in enumerate(serializer.data)]
            response_data = {"data": stock_data, "invests": None}

        return Response(response_data)

class ChartDataAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,format=None):
        frequency = request.GET.get("frequency")

        frequency_map = {
            "D": dayData,
            "W": weekData,
            "M": monthData,
            "Y": yearData
        }

        response_data = frequency_map.get(frequency)
        if response_data is None:
            raise ValidationError("frequency가 유효한 값이 아닙니다.")

        return Response(response_data)