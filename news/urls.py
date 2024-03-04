from django.urls import path

from news import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:id>/', views.news_detail, name='news_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='news_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    path('add/', views.create_news, name='news_add')
]