from django.urls import path
from . import views

urlpatterns = [
    path('web_applications/', views.web_applications, name='web_applications'),
    path('web_app_1/', views.web_app_1, name='web_app_1'),
    path('web_app_2/', views.web_app_2, name='web_app_2'),
    path('web_app_3/', views.web_app_3, name='web_app_3'),
]