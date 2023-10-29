from django.shortcuts import render
from django.http import HttpResponse


def index(request): # HttpRequest
    return HttpResponse('Страница приложения women')


def categories(request):
    return HttpResponse('<h1>статьи по категориям</h1')