from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Like

from .forms import ProfileForm, RegisterForm

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect("feed")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    is_following = request.user.following.filter(pk=user.pk).exists() if request.user != user else False
    liked_ids = set(Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True))
    return render(request, "accounts/profile.html", {
        "profile_user": user,
        "posts": posts,
        "is_following": is_following,
        "liked_ids": liked_ids,
    })


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            new_pw = form.cleaned_data.get("new_password")
            if new_pw:
                user.set_password(new_pw)
                user.save()
                login(request, user)
                messages.success(request, "Senha alterada com sucesso.")
            messages.success(request, "Perfil atualizado.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow == request.user:
        return redirect("profile", username=username)
    if request.user.following.filter(pk=user_to_follow.pk).exists():
        request.user.following.remove(user_to_follow)
    else:
        request.user.following.add(user_to_follow)
    return redirect("profile", username=username)


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    return render(request, "accounts/user_list.html", {
        "profile_user": user,
        "user_list": followers,
        "title": "Seguidores",
    })


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    return render(request, "accounts/user_list.html", {
        "profile_user": user,
        "user_list": following,
        "title": "Seguindo",
    })
