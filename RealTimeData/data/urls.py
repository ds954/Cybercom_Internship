from django.urls import path
from .views import CommentView,comment_page,post_comment

urlpatterns=[
    path('',CommentView,name='comment'),
    path('ajax/', comment_page, name='comment_page'),
    path('post-comment/', post_comment, name='post_comment'),
]
