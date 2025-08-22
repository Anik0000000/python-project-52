# task_manager/views.py
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello from Hexlet Code!")