from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    # ✅ Fixed: Match the actual function name in views.py
    path('profile/<str:username>/', views.profile, name='profile'),

    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
