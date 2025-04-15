from django.shortcuts import render
from django.shortcuts import render





# Create your views here.

def index(request):
    return render(request, 'index.html',context= {'text':'hello world'})

def notification_page(request):
    return render(request,'notification_page.html')