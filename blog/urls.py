
from django.urls import path
from .views import (
	PostListView, 
	UserPostListView,
    LikeView,
    CreatePostView,
    UpdatePostView,
    DetailPostView 
	)
from . import views 

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', DetailPostView.as_view(), name = 'post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name='blog-about'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('post/new/', CreatePostView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', views.delete_post_info, name = 'post-delete'),
    #path('<slug:slug>/',PostDetailView.as_view(),name='post_detail')
]
