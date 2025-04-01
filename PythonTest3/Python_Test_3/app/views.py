from django.shortcuts import render,redirect
from .models import Employee,Department
from datetime import datetime,timedelta
from django.db.models import Count
from .forms import EmployeeForm,UserForm,ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import EmployeeSerializer
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def Retrive_data(request):
    last_30_days= datetime.now() - timedelta(days=30)
    department_employee_data=Department.objects.filter(department_name='IT')

   
    it_department = Department.objects.get(department_name="IT")
    it_employees = Employee.objects.filter(department=it_department)
    join_last_30=Employee.objects.filter(joined_date__gte=last_30_days)

    count_id=Employee.objects.values('department__department_name').annotate(total=Count('id'))
    print(count_id)
    # print(employee_data)
    print(join_last_30)

    context={
        'employee_data':it_employees,
        'join_last_30':join_last_30,
        'count_id':count_id
    }

    return render(request,'retrive_data.html',context)

# Question 5
def register_employee(request):
    form = EmployeeForm(request.POST or None)

    if form.is_valid():
        return render(request, 'success.html')  # Redirect to success page

    return render(request, 'register.html', {'form': form})




# Question 4
@api_view(['GET'])
def employee_list(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

# Question 6
def upload_profile(request):
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'success.html')
    else:
        form = ProfileForm()

    return render(request,'upload_profile.html',{'form':form})        


def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        print(username)
        print(password)
        user=authenticate(username=username,password=password)
        print(user)
        if user:
            print("user is not none")
            return render(request,'dashboard.html')
        
    return render(request,'login.html')  


@login_required
def dashboard(request):
    print(request.user)
    if request.user.is_authenticate is None:
        return redirect('login')
    return render(request,'dashboard.html') 

def logout(request):
    request.session.flush()
    return redirect('login') 


# Question 9
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer   

# Question 11
@csrf_exempt   
def submit_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

        form = UserForm(data)
        
        if form.is_valid():
            return JsonResponse({
                'status': 'success',
                'message': 'Form submitted successfully!',
                'data': form.cleaned_data
            }, status=200)

        return JsonResponse({
            'status': 'error',
            'message': 'Form validation failed.',
            'errors': form.errors
        }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)