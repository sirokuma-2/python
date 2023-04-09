from django.urls import path,include
from blog import views

app_name="blog"

urlpatterns = [
    path('',views.index),
    path('article_form/', views.create_article, name="create_article"), #記事投稿ページのURLパス
    path('tags/<slug:slug>/',views.tags),
    path('<slug:pk>/',views.article,name="article"),
    path('<slug:pk>/like/',views.like),
    
]
   