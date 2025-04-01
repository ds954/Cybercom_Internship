from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',Retrive_data,name='retrive_data'),
    path('register/',register_employee,name="register"),
    path('upload_profile/',upload_profile,name="upload_profile"),
    path('login/',login,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logout/',logout,name='logout'),
    # path('employee_data/',employee_data,name='employee_data'),
    path('api/employees/', employee_list, name='employee-list'),
    path('api/employees_data/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees_data/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('submit-form/',submit_form,name='submit_form')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)