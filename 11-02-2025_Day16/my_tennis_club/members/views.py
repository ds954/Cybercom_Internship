from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
    return render(request,'hello.html',{'name':'Dhara'})


def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template=loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'x':0,
    'color':'red',
    'fruits': ['Apple', 'Banana', 'Cherry']
  }
  return HttpResponse(template.render(context, request))

def tags(request):
  mymembers = Member.objects.all().values()
  template=loader.get_template('tags.html')
  context={
    # 'Greeting':5,
    'members': mymembers,
  }
  return HttpResponse(template.render(context,request))

def home(request):
  template=loader.get_template('home.html')
  return HttpResponse(template.render())

def car(request):
  template = loader.get_template('car.html')
  context = {
    'cars': [
      {
        'brand': 'Ford',
        'model': 'Mustang',
        'year': '1964',
      },
      {
        'brand': 'Ford',
        'model': 'Bronco',
        'year': '1970',
      },
      {
        'brand': 'Ford',
        'model': 'Sierra',
        'year': '1981',
      },
      {
        'brand': 'Volvo',
        'model': 'XC90',
        'year': '2016',
      },
      {
        'brand': 'Volvo',
        'model': 'P1800',
        'year': '1964',
      }]
    }
  return HttpResponse(template.render(context, request))

def filter(request):
  template=loader.get_template('filter.html')
  context={
    'fruits': ['apple', 'banana','', 'cherry',None],
    'vegetables':'potato',
    'name':'xyz\s error',
    "x":0,
    "y":15,
    "size":1024
  }
  return HttpResponse(template.render(context,request))