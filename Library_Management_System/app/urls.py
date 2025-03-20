from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
# from app.admin import custom_admin


urlpatterns=[
    path('register/',views.register_view,name='register'),
    path('refresh-token/', views.refresh_token_view, name='refresh_token'),
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
    path('notification/',views.notification,name='notification'),
    path('about/',views.about,name='about'),
    path('privacy/',views.privacy,name='privacy'),
    path('terms/',views.terms,name='terms'),
    path('contact/',views.contact,name='contactus'),
    path('user_book/',views.user_book,name='user_book'),
    path('user_duebook/',views.user_duebook,name='user_duebook'),
    path('pending_renewal/',views.pending_renewal,name='pending_renewal'),
    path('pending_request/',views.pending_request,name='pending_request'),
    path('returned_books/',views.returned_book,name='returned_books'),
    path('logout/', views.logout_view, name='logout'),
    # path('custom_admin_login/', views.custom_admin_login, name='custom_admin_login'),    
    path('custom-admin/login/', views.custom_admin_login, name='custom_admin_login'),

     path('custom-admin/dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('custom-admin/books/', views.custom_books, name='custom_books'),
    path('custom-admin/books/add/', views.custom_book_add, name='custom_book_add'),
    path('custom-admin/borrow-request/<int:request_id>/update/', views.update_borrow_request_status, name='custom_borrow_request_update'),
    path('custom-admin/borrow/',views.admin_borrow_request,name='admin_borrow_request'),
    path('custom-admin/user/',views.admin_user,name='admin_user'),
    path('custom-admin/notification/',views.admin_notification,name='admin_notification'),
    path('custom-admin/issued_book/',views.admin_issued_book,name='admin_issued_book'),
    path('custom-admin/returned_book/',views.admin_returned_book,name='admin_returned_book'),
    path('custom-admin/non_returned_book/',views.admin_not_returned_book,name='admin_not_returned_book'),
    path('custom-admin/pending_renewal/',views.admin_pending_renewal_request,name='admin_pending_renewal_request'),
    path('custom-admin/borrow_history',views.admin_borrow_history,name='admin_borrow_history'),
    # path('custom-admin/', custom_admin.urls),

       path('custom-admin/members/', views.manage_members, name='manage_members'),
    path('custom-admin/members/add/', views.add_member, name='add_member'),
    path('admin/members/edit/<int:user_id>/', views.edit_member, name='edit_member'),
    path('admin/members/delete/<int:user_id>/', views.delete_member, name='delete_member'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)