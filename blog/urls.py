from django.urls import path
from . import views
from .views import PostListView, PostDetailView, userPostListView, PostCreateView, PostUpdateView, PostDeleteView
from users import views as user_views


urlpatterns = [
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', userPostListView.as_view(), name='user-posts'),
    path('register/', user_views.register, name='user_views'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),




]
