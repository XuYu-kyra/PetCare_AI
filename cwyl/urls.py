from django.urls import path
from cwyl import views

urlpatterns = [
    path('', views.index, name='index'),  # 定义根路径视图
    path('buildindex/', views.buildindex, name='buildindex'),  # 定义buildindex视图
    path('questionAnswering/', views.questionAnswering, name='questionAnswering'),
    path('searchanswer', views.searchanswer, name='searchAnswer'),
    
]
