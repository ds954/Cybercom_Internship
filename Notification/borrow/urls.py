from django.urls import path
from .views import user_borrow_request, update_request_status

urlpatterns = [
    path("", user_borrow_request, name="borrow_request"),
    path("update-request/<int:request_id>/<str:action>/", update_request_status, name="update_request_status"),
]
