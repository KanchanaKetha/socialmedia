from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm
from posts.models import Post  # To show user's posts in profile

# Register new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Profile View
@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(user=profile_user.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user.user,
        'profile': profile_user,
        'posts': posts
    })


# Profile Edit
@login_required
def edit_profile(request, username):
    if request.user.username != username:
        return redirect('profile', username=request.user.username)

    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


# Account Delete
@login_required
def delete_account(request, username):
    if request.user.username != username:
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('register')
    return redirect('profile', username=request.user.username)

