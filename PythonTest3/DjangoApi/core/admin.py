from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['name','email','department','joined_date']

admin.site.register(Department)
admin.site.register(EmployeeProfile)
admin.site.register(User)