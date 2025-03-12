from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('register/',views.register_view,name='register'),
    path('',views.login_view,name='login'),
    path('otp/<int:user_id>',views.verify_otp,name='verify-otp'),
    path('book/', views.book_list, name='book'),
    path('email/',views.email,name='email'),
    path('otp/<int:user_id>/',views.otp_password,name='otp'),
    path('reset_password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('view_profile/',views.view_profile,name="view_profile"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_books, name='search_books'),
    path('borrow_history/', views.borrow_history, name='borrow_history'),
    path('request_renewal/<int:request_id>/', views.request_renewal, name='request_renewal'), 
    path('cancel_request/<int:request_id>/', views.cancel_book, name='cancel_book'), 
    path('return_book/<int:request_id>/', views.return_book, name='return_book'),
    path('request_book/<int:book_id>/', views.request_book, name='request_book'),
    path('returned-books/', views.returned_books, name='returned_books'),
    path('canceled-books/', views.canceled_books, name='canceled_books'),
    path('renewal-books/', views.renewal_books, name='renewal_books'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path('notification/',views.notification,name='notification')


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)