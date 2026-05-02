from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from posts.models import Post


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Pulse, {user.username}! Your account has been created.')
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'feed')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    is_following = profile.is_followed_by(request.user)
    is_own_profile = request.user == profile_user

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'posts_count': posts.count(),
        'followers_count': profile.get_followers_count(),
        'following_count': profile.get_following_count(),
        'is_following': is_following,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    profile = target_user.profile
    if profile.is_followed_by(request.user):
        profile.followers.remove(request.user)
        is_following = False
        action = 'unfollowed'
    else:
        profile.followers.add(request.user)
        is_following = True
        action = 'followed'

    return JsonResponse({
        'is_following': is_following,
        'action': action,
        'followers_count': profile.get_followers_count(),
    })


@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = profile_user.profile.followers.all()
    return render(request, 'users/followers_list.html', {
        'profile_user': profile_user,
        'users_list': followers,
        'list_type': 'Followers'
    })


@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = Profile.objects.filter(followers=profile_user)
    following_users = [p.user for p in following]
    return render(request, 'users/followers_list.html', {
        'profile_user': profile_user,
        'users_list': following_users,
        'list_type': 'Following'
    })


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk)[:10]
    return render(request, 'users/search.html', {'users': users, 'query': query})
