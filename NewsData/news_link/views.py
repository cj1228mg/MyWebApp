import requests
import csv
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse

from .forms import SearchKeywordForm, FileNameForm

def get_news(keyword, limit):
    url = "https://news.yahoo.co.jp/search/"

    res = requests.get(url + "?p=" + keyword + "&ei=utf-8")
    soup = BeautifulSoup(res.text, "html.parser")

    li_elem = soup.find_all("li", attrs={"class": "newsFeed_item"}, limit=limit)

    news_title_link = []

    for elem in li_elem:
        title_news_dict = {}
        try:
            title_news_dict["タイトル"] = elem.find(attrs={"class": "newsFeed_item_title"}).text
            title_news_dict["リンク"] = elem.find("a").get("href")
            news_title_link.append(title_news_dict)
        except AttributeError:
            pass
    
    return news_title_link

def create_csvfile(file_name, data):
    field_name = ["タイトル", "リンク"]

    # エラー
    # path = f"C:\Users\c0b20201c8\Desktop\djangoStudy\MyProject\NewsLink_BeautifulSoup\csv_file\{file_name}"
    # 原因：\がエスケープシーケンスとして見なされているから

    path = f"C:\\Users\\c0b20201c8\\Desktop\\djangoStudy\\MyProject\\NewsLink_BeautifulSoup\\csv_file\\{file_name}.csv"

    with open(path, "w", encoding="utf_8_sig", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(data)

def index(request):
    ctxt = {}
    
    if request.method == "GET":
        ctxt['tab_title'] = "ニュースのリンクを取得しよう！"
        ctxt['form_search_keyword'] = SearchKeywordForm

        return render(request, "news_link/index.html", ctxt)

    if request.method == "POST":
        form_search_keyword = SearchKeywordForm(request.POST or None)

        if form_search_keyword.is_valid():

            keyword = form_search_keyword.cleaned_data['keyword']
            news_title_link = get_news(keyword, 10)
            
            ctxt['tab_title'] = f"{keyword}のニュースを取得する"
            ctxt['keyword'] = keyword
            ctxt['form_search_keyword'] = SearchKeywordForm(initial={"keyword": keyword})
            ctxt['form_file_name'] = FileNameForm
            ctxt['news_title_link'] = news_title_link

        return render(request, "news_link/index.html", ctxt)

def download_csv(request, keyword):
    ctxt = {}

    if request.method == "POST" and ("create_csvfile" in request.POST):

        form_file_name = FileNameForm(request.POST or None)
        news_title_link = get_news(keyword, 10)

        if form_file_name.is_valid():
            file_name = form_file_name.cleaned_data['file_name']

            create_csvfile(file_name, news_title_link)

            ctxt['news_title_link'] = news_title_link

            ctxt['form_file_name'] = FileNameForm
            ctxt['message'] = f"{keyword}についてのニュースをcsvファイルに変換しました。"
            ctxt['news_title_link'] = news_title_link
        else:
            ctxt['form_file_name'] = FileNameForm(request.POST or None)

        ctxt['tab_title'] = f"{keyword}をcsvに変換します"
        ctxt['keyword'] = keyword
        ctxt['form_search_keyword'] = SearchKeywordForm(initial={"keyword": keyword})
        ctxt['news_title_link'] = news_title_link
        

        return render(request, "news_link/index.html", ctxt)
