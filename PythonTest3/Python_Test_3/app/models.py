from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class Department(models.Model):
    department_name=models.CharField(max_length=255)

    def get_employees(self):
        """ Returns all employees in this department. """
        return ", ".join([employee.name for employee in self.employees.all()])

    def __str__(self):
        return f'{self.department_name}'

class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    department=models.ManyToManyField(Department,related_name='employees',)
    joined_date=models.DateField(default=now)
    Designation=models.CharField(default='Data Engineer', null=True,max_length=255)

    
    def __str__(self):
        return f'{self.name}'

class EmployeeProfile(models.Model):
    Employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='profile_pics/')

class User(models.Model):
    username=models.CharField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=20)

