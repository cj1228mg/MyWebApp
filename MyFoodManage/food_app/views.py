import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Food, Category
from .forms import SearchForm, AddFoodForm

# ホーム画面
def index(request):
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime("%Y-%m-%d")
    
    ctxt = {}

    if request.method == "GET":

        ctxt['tab_title'] = "食材を管理して、無駄にならないようにしよう！"

        # 賞味期限と消費期限を昇順に取り出す
        food_expiry_date = Food.objects.order_by("expiry_date")
        food_expiration_date = Food.objects.order_by("expiration_date")

        expiry_date_list = []
        expiration_date_list = []

        # 賞味期限と消費期限が切れてる食材をリストに追加
        for food in food_expiry_date:
            if food.expiry_date is not None:
                if str(food.expiry_date) < dt_now:
                    expiry_date_list.append(food)

        for food in food_expiration_date:
            if food.expiration_date is not None:
                if str(food.expiration_date) < dt_now:
                    expiration_date_list.append(food)

        ctxt["expiry_date_list"] = expiry_date_list
        ctxt["expiration_date_list"] = expiration_date_list
        
        return render(request, "food_app/index.html", ctxt) 

    else:
        return HttpResponse("不正なメソッドです", status=5)

# def about_food_app(request):
#     ctxt = {}

#     if request.method == "GET":
#         ctxt["tab_title"] = "このアプリについて"

#         return render(request, "food_app/about_food_app.html", ctxt)

# 食材の詳細
def food_detail(request, food_id):
    ctxt = {}

    if request.method == "GET":
        food_data = Food.objects.get(uuid=food_id)
        ctxt["tab_title"] = f"{food_data.name}の詳細"
        ctxt["food_data"] = food_data

        return render(request, "food_app/food_detail.html", ctxt)

# 食材の一覧
def food_list(request, food_str):
    ctxt = {}

    if request.method == "GET":

        food_list = []
        food_list = Food.objects.all()

        expiry_date_list = []
        expiration_date_list = []

        for food in food_list:
            if food.expiry_date is not None:
                expiry_date_list.append(food)
            elif food.expiration_date is not None:
                expiration_date_list.append(food)
            else:
                print("エラー")

        if food_str == "食材全一覧":
            ctxt['food_data'] = food_list
        elif food_str == "賞味期限の一覧":
            ctxt['food_data'] = expiry_date_list
        elif food_str == "消費期限の一覧":
            ctxt['food_data'] = expiration_date_list
        
        ctxt["tab_title"] = food_str
        ctxt["id_str"] = food_str

        return render(request, "food_app/food_list.html", ctxt)
    else:
        return HttpResponse("不正なメソッドです。", status=5)

# 食材を追加
def add_food(request):
    ctxt = {}

    if request.method == "GET":
        ctxt['tab_title'] = "新しい食材を追加"
        ctxt['page_headline'] = "食材を追加する"
        ctxt['form'] = AddFoodForm
        ctxt["method"] = request.method

        return render(request, "food_app/add_food.html", ctxt)
    
    elif request.method == "POST":
        form = AddFoodForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            expiry_date = form.cleaned_data["expiry_date"]
            expiration_date = form.cleaned_data["expiration_date"]
            memo = form.cleaned_data["memo"]

            # name = request.POST['name']
            # category = request.POST["category"]
            # expiry_date = request.POST["expiry_date"]
            # expiration_date = request.POST["expiration_date"]
            # memo = request.POST["memo"]

            category = Category.objects.get(category=category)
            
            if expiry_date == "":
                expiry_date = None
            
            if expiration_date == "":
                expiration_date = None

            food = Food.objects.create(
                name=name, 
                category=category, 
                expiry_date=expiry_date, 
                expiration_date=expiration_date,
                memo=memo
            )

            food.save()

        ctxt["message"] = "新しい食材を追加しました"
        ctxt["method"] = request.method

        return render(request, "food_app/add_food.html", ctxt) 
    else:
        return HttpResponse("不正なメソッドです。", status=5)

# 食材を削除
def delete_food(request, food_id):
    ctxt = {}

    if request.method == "GET":
        data = Food.objects.get(uuid=food_id)
        
        ctxt["tab_title"] = f"{data.name}を削除"
        ctxt['data_name'] = data.name
        ctxt["method"] = request.method

        return render(request, "food_app/delete_food.html", ctxt)
    
    elif request.method == "POST":
        data = Food.objects.get(uuid=food_id)
        data.delete()

        ctxt["tab_title"] = "削除完了"
        ctxt["message"] = f"{data.name}を削除しました"
        ctxt["method"] = request.method

        return render(request, "food_app/delete_food.html", ctxt)

    else:
        return HttpResponse("不正なメソッドです", status=5)

# 食材を更新
def update_food(request, food_id):
    ctxt = {}

    if request.method == "GET":
        food_data = Food.objects.get(uuid=food_id)

        # フォームにデータを渡す。
        initial_values = {
            'name': food_data.name,
            'category': food_data.category,
            'expiry_date': food_data.expiry_date,
            'expiration_date': food_data.expiration_date,
            'memo': food_data.memo
        }
        
        ctxt["tab_title"] = f"{food_data.name}を更新する"
        ctxt["page_headline"] = f"「{food_data.name}」を更新しますか？"
        ctxt["form"] = AddFoodForm(initial=initial_values)
        ctxt["method"] = request.method

        return render(request, "food_app/add_food.html", ctxt)

    elif request.method == "POST":
        form = AddFoodForm(request.POST or None)
        
        if form.is_valid():
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            expiry_date = form.cleaned_data["expiry_date"]
            expiration_date = form.cleaned_data["expiration_date"]
            memo = form.cleaned_data['memo']

            category = Category.objects.get(category=category)

            # この書き方をするとデータが追加される
            # food_data = Food.objects.create(
            #     name=name,
            #     category=category,
            #     expiry_date=expiry_date,
            #     expiration_date=expiration_date,
            #     memo=memo,
            # )

            # 更新を行う場合この書き方
            food_data = Food.objects.get(uuid=food_id)
            food_data.name = name
            food_data.category = category
            food_data.expiry_date = expiry_date
            food_data.expiration_date = expiration_date

            food_data.save()

        ctxt["tab_title"] = "更新完了"
        ctxt["method"] = request.method

        ctxt["message"] = "更新しました"

        return render(request, "food_app/add_food.html", ctxt)

    else:
        return HttpResponse("不正なメソッドです。", status=5)
            


