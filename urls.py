from django.urls import path
from .views import home, recommend_music  # 'recommendation' 앱의 views에서 함수를 임포트

urlpatterns = [
    path("", home, name="home"),
    path('recommend/', recommend_music, name='recommend_music'),
]
