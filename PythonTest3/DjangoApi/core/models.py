from django.db import models



class Department(models.Model):
    department_name=models.CharField(max_length=255)

    def __str__(self):
        return f'{self.department_name}'

class Employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    joined_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

class EmployeeProfile(models.Model):
    Employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    profile_picture=models.ImageField()

class User(models.Model):
    username=models.CharField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=20)

