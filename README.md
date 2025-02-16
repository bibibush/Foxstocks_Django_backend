# 증권 대시보드 웹사이트(백엔드)
##### 웹사이트 : https://foxstocks.site
##### 프론트엔드 상세 설명 : https://github.com/bibibush/react-vite-frontend

## 소개
> 네이버 증권 페이지를 크롤링하여 데이터를 가공 후, 프론트엔드로 넘겨주는 서버 측 로직을 Django를 사용해 구현했습니다.
>
> 현재 인기있는 주식들과 주식들의 시장가를 크롤링 또는 각 분야별 주식 순위 데이터를 크롤링 하여 딕셔너리 형태로 데이터를 가공하여 프론트엔드로 보내줍니다.
>
> 데이터베이스는 docker를 사용해 postgresql과 연동했습니다. 주식 데이터들과 사용자 데이터들을 csv로 다운로드 받고 python의 management기능을 사용해 명령어로 데이터베이스를 업데이트 할 수 있는 로직도 구현했습니다.
>
> 사용자 정보는 django에 내장된 User모델을 사용하지 않고 abstractUser클래스를 상속받아 프로필 이미지, 투자 내역등의 필드 들을 추가해 재정의 했습니다.
>
> 인증 방식은 django-rest-framework를 이용한 JWT인증 방식을 구현했습니다. 배포는 docker, gunicorn을 사용해 aws ec2에 배포했습니다.

<br />

## 사용 기술
* Python:3.12
* Django: 5.1
* Django-rest-framework
* Pandas
* Beautifulsoup4
* requests
* gunicorn
* Docker
* aws ec2

<br />

## 핵심 설명
<details>
  <summary><b>주식 모델의 작성과 크롤링 후, 데이터 가공</b></summary>

  먼저 django에서 stocks라는 앱을 생성 후, Stock 모델을 정의했습니다.
  ```python
  class Stock(models.Model):
    class StockColor(models.TextChoices):
        SAMSUNG_E = ("#A6F7E2","삼성전자")
        SK = ("#B79BFF","SK하이닉스")
        LG = ("#FFE5A5","LG에너지솔루션")
        SAMSUNG_B = ("#C7FFA5","삼성바이오로직스")
        HYUNDAI = ("#F8A5FF","현대차")

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    color = models.CharField(max_length=50,choices=StockColor.choices, default=StockColor.SAMSUNG_E)
    is_domestic = models.BooleanField()

    def __str__(self):
        return self.name
```
여기서 color필드는 choices를 적용했습니다. 이러면 데이터베이스에는 컬러의 헥스값이 들어가지만 admin사이트에는 '삼성전자'같은 라벨을 보여줍니다.

크롤링을 하기 위한 코드 작성을 보겠습니다.
stocks앱 디렉토리에 crawling.py파일을 생성한 뒤
```python
class NaverFinanceClass:
    def crawl(self,query):
        if query.is_domestic is True:
            url = f"https://finance.naver.com/item/main.naver?code={query.code}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            bsobj = BeautifulSoup(res.text, 'html.parser')
            content = bsobj.find("div", {"id": "content"})
            no_today = content.find("p", {"class": "no_today"})
            em = no_today.find("em")

            price = em.find("span", {"class": "blind"}).text

            no_exday = content.find("p",{"class":"no_exday"})
            no_up = no_exday.find("em",{"class":"no_up"})
            no_down = no_exday.find("em",{"class":"no_down"})

            if no_up is not None:
                increased = no_up.find("span",{"class":"blind"}).text
                decreased = None

            elif no_down is not None:
                increased = None
                decreased = no_down.find("span",{"class":"blind"}).text

            else:
                increased = None
                decreased = None

        else:
            url = f"https://www.google.com/finance/quote/{query.code}"
            price = "0"
            increased = None
            decreased= None

        return {"price":price,"increased":increased,"decreased":decreased}
```
NaverFinanceClass라는 클래스를 정의하고, 그 안에 crawl 메서드를 정의했습니다.
<br />
crawl메서드는 query를 매개변수로 받습니다. 이 query는 주식이 어떤 주식인지 구별하기 위해서 사용됩니다.

requests라이브러리를 pip로 설치한 후, get함수를 사용해 제공한 url로 부터 정보들을 가져옵니다. 이때 크롤링을 하는 주체가 봇이 아님을 밝히기 위해 요청 헤더에 'User-Agent'를 작성해줍니다.
<br />
이렇게 가져온 웹사이트 정보들을 BeautifulSoup클래스의 인자로 전달합니다. 두번째 인자로 html.parser을 작성해 줘야 텍스트 형식으로 된 html문서를 파싱할 수 있습니다.
<br />
파싱된 html의 정보를 가지고 있는 bs객체는 find와 find_all 메서드들을 통해 요소들을 취득할 수 있습니다. 이 메서드들은 첫번째 인자로 요소의 태그 두번째 인자로 요소의 어트리뷰트를 인자로 받습니다.

이렇게 취득한 요소들의 텍스트 노드를 가져와서 딕셔너리 형태로 가공합니다. 위의 코드에서는 {"price":price,"increased":increased,"decreased":decreased} 이렇게 딕셔너리를 작성해주었습니다.
<br />
price는 주식의 현재 가격, increased는 전일 대비 상승가, decreased는 전일 대비 하한가입니다.

이제, 브라우저로 부터 크롤링 된 주식 데이터를 요청받는 로직을 처리하기 위해, view.py 파일에 코드를 작성했습니다.
```python
class StockListView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,format=None):
        stocks = Stock.objects.all()
        crawling = NaverFinanceClass()

        serializer = StockSerializer(stocks, many=True)

        additional_data = [crawling.crawl(stock) for stock in stocks]
        stock_data = [{**stock, **additional_data[index]} for index, stock in enumerate(serializer.data)]
        response_data = {"data": stock_data}

        return Response(response_data)
```
작성한 StockListView는 drf의 APIView 클래스를 상속받습니다. 이 View는 로그인하지 않은 사용자도 볼 수 있기 때문에 permission_classes를 AllowAny로 설정했습니다.
<br />
브라우저로부터 get요청을 받으면 아까 작성했던 Stock모델에서 모든 쿼리를 가져옵니다. 그리고 StockSerializer를 통해 가져온 모든 쿼리를 시리얼라이징 처리합니다.
<br />
StockSerializer는 모델 시리얼라이저를 사용합니다.
```python
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"
```
리스트 컴프리헨션을 사용해서 각 주식들을 크롤링한 후 가공된 데이터를 리스트에 담아줍니다.
<br />
이제 시리얼라이저된 데이터와 크롤링 된 데이터를 합쳐서 데이터리스트 형태로 만들어 stock_data에 할당합니다. 그리고 브라우저에 {"data":stock_data} 형태로 데이터를 보내줍니다.

브라우저는 
<img src="./staticfiles/스크린샷 2025-02-16 122825.png" alt="주식 데이터들" />
이렇게 크롤링된 주식 데이터들을 보여줄 수 있습니다.
</details>

<br />

<details>
  <summary><b>사용자 투자 내역 모델 작성 (Meta 클래스를 사용해서 유니크 제약 구현)</b></summary>

  먼저 Invested라는 모델을 작성했습니다.
  ```python
  class Invested(models.Model):
    input = models.PositiveIntegerField()
    initial_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField()
    company = models.ForeignKey("stocks.Stock",on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user","company"],name="accounts_invested_uniq")
        ]
    def __str__(self):
        return f"{self.user.username} - {self.company}"
```
이 모델은 앞서 정의한 Stock모델과 User모델을 다대일 관계로 가집니다. User모델은 abstractUser클래스를 상속받아 재정의 했습니다.
```python
class User(AbstractUser):
    email = models.EmailField(_("email address"),unique=True)
    profile_img = models.ImageField(upload_to="profile_img/", null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
```
</details>
