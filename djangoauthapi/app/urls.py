# urls.py
from django.urls import path
from app.views import LoginView,LogoutView,AppUserListView,GetAccessTokenView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("app-users/", AppUserListView.as_view(), name="app-user-list"),
    path("get-access-token/", GetAccessTokenView.as_view(), name="get_access_token"),
]