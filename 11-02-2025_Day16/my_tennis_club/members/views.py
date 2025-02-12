from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Member
import datetime


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
    'vegetables':'potaTo',
    'name':'xyz\t error',
    "x":0,
    "y":15,
    "size":1024*1024,
    'text':"_Hello\nmy name is- Leo.\n\nI am a student.-",
    'arr':[0,1,2],
    'mytext': '<h1>Welcome to <b>MY</b>World!</h1>',   
    'date':datetime.datetime(2001,5,9,11,30),
    'birthday':datetime.datetime(2004,5,21,3,0),
    'newtext':'<h1> welcome to django tutorial.</h1>',
    'url':"https://www.w3schools.com/django/django_ref_filter.php"
  }
  return HttpResponse(template.render(context,request))

def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        member.firstname = request.POST.get("firstname")
        member.lastname = request.POST.get("lastname")
        member.phone = request.POST.get("phone")
        member.joined_date = request.POST.get("joined_date")
        member.save()
        return redirect('details', id=member.id)

    return render(request, 'edit.html', {'member': member})
