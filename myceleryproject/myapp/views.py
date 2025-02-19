from django.shortcuts import render
from myceleryproject.celery import add
from myapp.tasks import sub
from celery.result import AsyncResult

# def index(request):
#     print('Result: ')
#     ans=add.delay(5,8)
#     print("result is: ",ans)
#     ans1=sub.delay(5,8)
#     print("result1 is: ",ans1)
#     return render(request,'home.html')

def check_result(request, task_id):
    """Checks Celery task status and result."""
    result = AsyncResult(task_id)
    print('ready: ', result.ready())
    print('success: ', result.successful())
    print('fail: ', result.failed())
    return render(request, 'result.html', {'result': result})

def index(request):
    """Starts 'add' Celery task and shows task ID."""
    result = add.delay(5, 8)
    print("result is: ", result)
    return render(request, 'home.html', {'result': result})

def about(request):
    """Renders 'about.html'."""
    return render(request, 'about.html')

def contact(request):
    """Renders 'contact.html'."""
    return render(request, 'contact.html')