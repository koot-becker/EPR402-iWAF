from django.urls import path
from . import views

urlpatterns = [
    path('web_applications/', views.web_applications, name='web_applications'),
]