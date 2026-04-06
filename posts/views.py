from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Like, Post


@login_required
def feed(request):
    following_ids = request.user.following.values_list("id", flat=True)
    posts = Post.objects.filter(author_id__in=[*following_ids, request.user.id])
    liked_ids = Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True)
    form = PostForm()
    return render(request, "posts/feed.html", {
        "posts": posts,
        "form": form,
        "liked_ids": set(liked_ids),
    })


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    return redirect("feed")


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    liked = Like.objects.filter(user=request.user, post=post).exists()
    form = CommentForm()
    return render(request, "posts/post_detail.html", {
        "post": post,
        "comments": comments,
        "liked": liked,
        "form": form,
    })


@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    next_url = request.POST.get("next", request.META.get("HTTP_REFERER", "/"))
    return redirect(next_url)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect("post_detail", pk=pk)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
    return redirect("feed")


@login_required
def explore(request):
    posts = Post.objects.all()
    liked_ids = Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True)
    return render(request, "posts/explore.html", {
        "posts": posts,
        "liked_ids": set(liked_ids),
    })
