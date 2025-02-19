from django.shortcuts import render
from django.http import JsonResponse
from blog.tasks import sleep_well


def get_blog(request):
    data={
        'success':'true',
    }
    sleep_well(5)
    return JsonResponse(data)

