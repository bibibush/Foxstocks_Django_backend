import requests
from bs4 import BeautifulSoup


class NaverFinanceClass:
    def crawl(self,query):
        if query.is_domestic is True:
            url = f"https://finance.naver.com/item/main.naver?code={query.code}"
        else:
            url = f"https://m.stock.naver.com/worldstock/stock/{query.code}/total"

        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        bsobj = BeautifulSoup(res.text, 'html.parser')
        content = bsobj.find("div",{"id": "content"})
        no_today = content.find("p",{"class": "no_today"})
        em = no_today.find("em")
        price = em.find("span",{"class": "blind"}).text

        return price