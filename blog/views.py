from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, UpdateForm

from .models import Post, Category


class HomeView(ListView):
    model = Post
    template_name = "home.html"


def PostDetailView(request, pk):
    post = Post.objects.get(id=pk)
    cats = post.category.all().values("name", "pk")
    context = {
        "post": post,
        "cats": cats,
    }
    return render(request, "post_detail.html", context)


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = Post.objects.filter(category=context["category"].pk)
        posts = q.all()
        context["posts_in_category"] = posts
        return context


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_new.html"


class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = "post_edit.html"


class DeletePostView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
