import requests
from bs4 import BeautifulSoup


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
        else:
            url = f"https://www.google.com/finance/quote/{query.code}"
            price = "0"



        return price