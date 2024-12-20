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

    def crawl_data_table(self,category,*args,**kwargs):
        url = "https://finance.naver.com/sise/"
        res = requests.get(url,headers={"User-Agent": "Mozilla/5.0"})
        bsobj = BeautifulSoup(res.text,"html.parser")
        table = bsobj.find("table",{"id":category})
        ths = table.find("tr").find_all("th")
        columns = [th.text for th in ths]
        trs = table.find_all("tr")[2:]
        response_data = []

        for tr in trs:
            if tr.find("td",{"class":"number"}):
                args_dict = {
                    arg: tr.find_all("td",{"class":"number"})[index + 5].text
                    for index,arg in enumerate(args)
                }

                response_dict = {
                    "name": tr.find("a",{"class":"tltle"}).text,
                    "current_price":tr.find_all("td",{"class":"number"})[2].text,
                    "from_yesterday": tr.find_all("td",{"class":"number"})[3].find("span",recursive=False).text,
                    "increased_percent": tr.find_all("td",{"class":"number"})[4].find("span").text,
                    **args_dict
                }
                response_data.append(response_dict)

        return {"columns":columns, "data":response_data,"total_count": len(trs)}