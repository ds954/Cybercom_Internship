from django.shortcuts import render
from django.http import response
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Employee,Department
from .Serilizers import *
# Create your views here.


# Function-Based View (FBV) to retrieve all employees in JSON format
def get_all_employees(request):
    # Fetch all employee records
    employees = Employee.objects.all()
    
    # Serialize the data into JSON format
    employee_list = list(employees.values( 'name', 'email', 'department','joined_date'))
    
    # Return the JSON response
    return JsonResponse({"employees": employee_list}, safe=False)

# Class-Based View (CBV) to display a list of departments
class DepartmentListView(ListView):
    model = Department
    template_name = 'departments_list.html'
    context_object_name = 'departments'

    def get_data(self):
        return Department.objects.all()


     


