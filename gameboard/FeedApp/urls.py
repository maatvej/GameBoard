from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('my_posts/', MyPosts.as_view(), name='my_posts'),
    path('replies_to_my_posts', RepliesList.as_view(), name='replies_to_posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('createpost', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/createreply', ReplyCreate.as_view(), name='reply_create'),
    path('<int:post_id>/<int:reply_id>/', views.reply_accept, name='reply_accept'),
    path('replies/<int:pk>', ReplyDetail.as_view(), name='reply_detail'),

]