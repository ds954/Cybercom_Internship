from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,TaskForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Task
from django.http import JsonResponse

def register_view(request):
    if request.method=='POST':
        registerform=RegisterForm(request.POST)
        if registerform.is_valid():
            user=registerform.save()
            return redirect('/')

    else:
        registerform=RegisterForm()
    return render(request,'register.html',{'form':registerform})    

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})        

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(complete=True)
    elif status == 'pending':
        tasks = tasks.filter(complete=False)
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.complete = not task.complete
        task.save()
        return JsonResponse({'status': 'success', 'complete': task.complete})
    return redirect('task_list')

def logout_view(request):
    logout(request)           # Logs out the user
    request.session.flush()   # Clears the session completely
    return redirect('login')  # Redirect to login page