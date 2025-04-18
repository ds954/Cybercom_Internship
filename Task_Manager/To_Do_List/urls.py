from django.urls import path
from .views import register_view,login_view,task_list,task_create,task_delete,task_update,task_toggle,logout_view

urlpatterns=[
    path('',login_view,name='login'),
    path('register/',register_view,name='register'),
    path('my_task/',task_list,name="task_list"),
    path('task_create/',task_create,name="task_create"),
     path('tasks/<int:pk>/edit/', task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle/', task_toggle, name='task_toggle'),
    path('logout/', logout_view, name='logout'),
]