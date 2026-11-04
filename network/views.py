from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Like, Follow, Profile

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("feed")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account has been created.")
        return redirect("feed")
    return render(request, "network/signup.html", {"form": form})

@login_required
def feed_view(request):
    posts = Post.objects.select_related("author").prefetch_related("comments", "likes")
    post_form = PostForm()
    comment_form = CommentForm()
    liked_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
    following_ids = set(Follow.objects.filter(follower=request.user).values_list("following_id", flat=True))
    return render(request, "network/feed.html", {
        "posts": posts, "post_form": post_form, "comment_form": comment_form,
        "liked_ids": liked_ids, "following_ids": following_ids,
    })

@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post has been published.")
    else:
        messages.error(request, "Please check your post details.")
    return redirect("feed")

@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        messages.error(request, "You can only delete your own posts.")
    else:
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect("feed")

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("feed")

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("profile", username=username)
    relation, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        relation.delete()
    return redirect(request.POST.get("next") or "profile", username=username) if request.POST.get("next") != "feed" else redirect("feed")

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    if request.method == "POST" and request.user == profile_user:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile", username=username)
    else:
        form = ProfileForm(instance=profile) if request.user == profile_user else None
    return render(request, "network/profile.html", {
        "profile_user": profile_user, "profile": profile, "form": form,
        "is_following": is_following, "posts": profile_user.posts.all(),
        "followers_count": profile_user.follower_links.count(),
        "following_count": profile_user.following_links.count(),
    })
