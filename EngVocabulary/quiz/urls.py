from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('word-list/<str:category>/', views.WordsListView.as_view(), name='word-list'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('flashcard/<str:category>/', views.FlashCardView.as_view(), name='flashcard'),
    path('words-mean/<str:category>/<int:pk>/', views.words_mean, name='words-mean'),
    path('start-quiz/<str:category>/', views.start_quiz, name='start-quiz'),
    path('result/<str:category>/<str:message>/<int:pk>/', views.ResultView.as_view(), name='result'),
    path('quiz/<str:category>/<int:pk>/', views.QuizView.as_view(), name='quiz'),
]