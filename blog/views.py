from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PostForm, UpdateForm

from .models import Post, Category, Rating


class HomeView(ListView):
    model = Post
    template_name = "home.html"


def PostDetailView(request, pk):
    post = Post.objects.get(id=pk)
    cats = post.category.all().values("name", "pk")
    rating = Rating.objects.filter(post=post).aggregate(Avg("rating"))["rating__avg"]
    context = {
        "post": post,
        "cats": cats,
        "rating": rating,
    }
    return render(request, "post_detail.html", context)


# def RatePostView(request, pk):
#     return render(request, "post_rate.html")


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
