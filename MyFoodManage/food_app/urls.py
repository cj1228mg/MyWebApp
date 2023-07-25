from django.urls import path

from . import views

app_name = "food_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("food-detail/<uuid:food_id>/", views.food_detail, name="food_detail"),
    # path("about-food-app/", views.about_food_app, name="about_food_app"),
    path("food-list/<str:food_str>/", views.food_list, name="food_list"),
    path("add-food/", views.add_food, name="add_food"),
    path("update-food/<uuid:food_id>/", views.update_food, name="update_food"),

    # 主キーにuuidを使用する場合、<uuid:変数名>にする
    path("delete-food/<uuid:food_id>/", views.delete_food, name="delete_food")
]