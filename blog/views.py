from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, UpdateForm

from .models import Post, Category, Rating

def get_top_rated_posts():
    top_posts = Post.objects.filter(Q(rating__rating__isnull=False) & Q(rating__rating__gt=0)).annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:5]
    return top_posts

class HomeView(ListView):
    model = Post
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_posts = get_top_rated_posts()
        context["top_posts"]= top_posts
        return context

    



class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        cats = Category.objects.filter(post=post.pk)
        context["cats"] = cats
        return context


def RatePostView(request, pk):
    post = Post.objects.get(id=pk)
    post_rating = Rating(
        rating=request.POST["rate"], post_id=post.pk, user=request.user
    )
    post_rating.save()

    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": pk}))


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


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ("title", "body", "category")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = "post_edit.html"


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
