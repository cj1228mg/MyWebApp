from django.urls import path

from . import views

app_name = "news_link"

urlpatterns = [
    path('', views.index, name='index'),
    path('download-csv/<str:keyword>/', views.download_csv, name="download_csv")
]