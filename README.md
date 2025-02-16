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
</details>
