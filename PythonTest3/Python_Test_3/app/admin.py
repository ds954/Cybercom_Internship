from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['name','email','joined_date','get_departments']
    filter_horizontal = ('department',)  # Allows selecting multiple departments

    def get_departments(self, obj):
        return ", ".join([dept.department_name for dept in obj.department.all()])
    
    get_departments.short_description = "Department"

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'get_employees')

admin.site.register(EmployeeProfile)
admin.site.register(User)