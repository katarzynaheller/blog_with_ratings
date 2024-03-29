from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    HomeView,
    CategoryListView,
    PostDetailView,
    RatePostView,
    CategoryDetailView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/rate/", RatePostView, name="post_rate"),
    path("post/<int:pk>/edit/", UpdatePostView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="post_delete"),
    path("post/new/", CreatePostView.as_view(), name="post_new"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
