import requests
from bs4 import BeautifulSoup

def get_news():
    url = "https://news.yahoo.co.jp/search/"
    keyword = "ウクライナ"

    res = requests.get(url + "?p=" + keyword + "&ei=utf-8")
    soup = BeautifulSoup(res.text, "html.parser")

    li_elem = soup.find_all("li", attrs={"class": "newsFeed_item"}, limit=5)

    news_title_link = {}

    for elem in li_elem:
        try:
            title = elem.find(attrs={"class": "newsFeed_item_title"}).text
            news_title_link[title] = elem.find("a").get("href")
        except AttributeError:
            pass
    
    return news_title_link

news_title_link = get_news()
print(news_title_link)