from django.urls import path
from .views import get_all_employees, DepartmentListView

urlpatterns = [
    path('employees/', get_all_employees, name='employee-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
]