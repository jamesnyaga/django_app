from django.urls import path
from . import views
from .views import PostListView, PostDetailView, userPostListView, PostCreateView, PostUpdateView, PostDeleteView
from users import views as user_views


urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', userPostListView.as_view(), name='user-posts'),
    path('register/', user_views.register, name='user_views'),
    path('about/', views.about, name='blog-about'),
]
