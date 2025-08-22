# task_manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]