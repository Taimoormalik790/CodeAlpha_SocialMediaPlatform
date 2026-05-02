from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from users.models import Profile


@login_required
def feed_view(request):
    # Get users the current user follows
    following_profiles = Profile.objects.filter(followers=request.user)
    following_users = [p.user for p in following_profiles]
    following_users.append(request.user)  # Include own posts

    posts = Post.objects.filter(author__in=following_users).select_related(
        'author', 'author__profile'
    ).prefetch_related('likes', 'comments')

    comment_form = CommentForm()

    # Annotate posts with user-specific data
    posts_data = []
    for post in posts:
        posts_data.append({
            'post': post,
            'is_liked': post.is_liked_by(request.user),
            'likes_count': post.get_likes_count(),
            'comments_count': post.get_comments_count(),
        })

    post_form = PostForm()
    suggested_users = User.objects.exclude(
        pk__in=[u.pk for u in following_users]
    ).exclude(pk=request.user.pk).select_related('profile')[:5]

    context = {
        'posts_data': posts_data,
        'post_form': post_form,
        'comment_form': comment_form,
        'suggested_users': suggested_users,
    }
    return render(request, 'posts/feed.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('feed')
    return redirect('feed')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author', 'author__profile')
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', pk=pk)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': post.is_liked_by(request.user),
        'likes_count': post.get_likes_count(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('feed')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('feed')


@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.is_liked_by(request.user):
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': post.get_likes_count(),
    })


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'content': comment.content,
                        'author': comment.author.username,
                        'author_pic': comment.author.profile.profile_picture.url if comment.author.profile.profile_picture else '',
                        'created_at': comment.created_at.strftime('%b %d, %Y'),
                    },
                    'comments_count': post.get_comments_count(),
                })
    return redirect('post_detail', pk=pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    return redirect('post_detail', pk=post_pk)


@login_required
def explore_view(request):
    posts = Post.objects.all().select_related(
        'author', 'author__profile'
    ).prefetch_related('likes', 'comments')

    posts_data = []
    for post in posts:
        posts_data.append({
            'post': post,
            'is_liked': post.is_liked_by(request.user),
            'likes_count': post.get_likes_count(),
            'comments_count': post.get_comments_count(),
        })

    return render(request, 'posts/explore.html', {'posts_data': posts_data})
