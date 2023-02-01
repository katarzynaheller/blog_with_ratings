from django.urls import path
from .views import (
    HomeView,
    CategoryListView,
    PostDetailView,
    CategoryDetailView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/<int:pk>/", PostDetailView, name="post_detail"),
    path("post/<int:pk>/edit/", UpdatePostView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="post_delete"),
    path("post/new/", CreatePostView.as_view(), name="post_new"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
]
