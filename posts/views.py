from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


# -----------------------------
# HOME FEED
# -----------------------------
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'posts/home.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids
    })


# -----------------------------
# CREATE POST
# -----------------------------
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your post has been created!")
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


# -----------------------------
# POST DETAIL + COMMENTS
# -----------------------------
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'form': form,
        'comments': comments,
        'liked_post_ids': liked_post_ids
    })


# -----------------------------
# LIKE / UNLIKE POST
# -----------------------------
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:  # Already liked → unlike
        like.delete()

    return HttpResponseRedirect(reverse('home'))


# -----------------------------
# PROFILE VIEW
# -----------------------------
@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')

    return render(request, 'posts/profile.html', {
        'profile_user': user_profile,
        'posts': posts
    })


# -----------------------------
# DELETE COMMENT
# -----------------------------
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user == request.user or request.user == comment.post.user:
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    else:
        messages.error(request, "You are not allowed to delete this comment.")

    return redirect('post_detail', post_id=comment.post.id)


# -----------------------------
# DELETE POST
# -----------------------------
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.user:
        post.delete()
        messages.success(request, "Your post has been deleted successfully.")
    else:
        messages.error(request, "You are not allowed to delete this post.")

    return redirect('home')
