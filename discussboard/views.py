from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Post, Comment, LikedComment
from discussboard.forms import CommentForm, LikedCommentForm, PostForm
from django.views.generic import RedirectView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max




# Create your views here.


def postList(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # posts = Post.objects.all()
    # post = get_object_or_404(Post, pk=pk)
    # if request.method == 'POST':
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.published_date = timezone.now()
    #         post.save()
    #         # have to add redirect so that it wont pass the data twice when refreshing the page *super important*
    #         return redirect('posts')
    #         # ('postDetail',pk=post.pk) if you want it to redirect to the new post detail page.
    # else:
    #     form = PostForm()
    frontEndStuff = {
        'posts': posts,
            # 'form': form,
        # 'post':post,
        }

    return render(request, 'posts/posts.html', frontEndStuff)

@login_required(login_url='/admin/login/')
def NewPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # have to add redirect so that it wont pass the data twice when refreshing the page *super important*
            return redirect('posts')
            # ('postDetail',pk=post.pk) if you want it to redirect to the new post detail page.
    else:
        form = PostForm()
        frontEndStuff = {
            'form': form,
        }

    return render(request, 'posts/posts.html', frontEndStuff)


def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comment = post.comments.all()
    comments = comment.annotate(like_count=Count('liked')).order_by('-like_count', '-created_date')

    # comments = Comment.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    # user = request.user

    
    # if request.method == 'POST':
    #     form = CommentForm(request.POST or None)
    #     likeform = LikedCommentForm(request.POST or None)

    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.author = request.user
    #         comment.created_date = timezone.now()
    #         comment.post = post
    #         comment.save()
    #         return redirect('postDetail', pk=post.pk)
            
    # else:
    form = CommentForm()
        # likeform = LikedComment()
    frontEndStuff = {
            'post': post,
            'form': form,
            'comments': comments,
            # 'likeform': likeform,
        }
    return render(request, 'posts/postDetail.html', frontEndStuff)


@login_required(login_url='/admin/login/')
def NewComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        likeform = LikedCommentForm(request.POST or None)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.created_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('postDetail', pk=post.pk)
            
    else:
        form = CommentForm()
        likeform = LikedComment()
        frontEndStuff = {
            'post': post,
            'form': form,
            'likeform': likeform,
        }
    return render(request, 'posts/postDetail.html', frontEndStuff)
    

@login_required(login_url='/admin/login/')
def postEdit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # comments = Comment.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    comment = post.comments.all()
    comments = comment.annotate(like_count=Count('liked')).order_by('-like_count','-created_date')

    if request.method == 'POST':
        # get the already posted discussion post updating existing form
        form = PostForm(request.POST, instance=post)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('postDetail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        comment = CommentForm()
        frontEndStuff = {
            'post': post,
            'form': form,
            'comments': comments,
        }
    return render(request, 'posts/postEdit.html', frontEndStuff)

@login_required(login_url='/admin/login/')
def CommentLike(request, pk):
    post = get_object_or_404(Comment, pk=pk)
    user = request.user
    commentClass = LikedCommentForm
    form  = commentClass(request.POST)
    if request.method == "POST":
        # if form.is_valid():
        commentID = request.POST.get('like_id')
        commentOBJ = Comment.objects.get(pk=commentID)

        if user in commentOBJ.liked.all():
            commentOBJ.liked.remove(user)
        else:
            commentOBJ.liked.add(user)

        like, created = LikedComment.objects.get_or_create(user=user, comment_id=commentID)

        if not created:
            if like.value == 'like':
                like.value = 'unlike'
            else:
                like.value = 'like'
                    
        like.save()
        
        return redirect('postDetail', pk=post.pk)
    else:
        likeform = LikedComment()
        frontEndStuff = {
            'likeform': likeform,
            # 'user': user,
        }
    
    return render(request, 'posts/postDetail.html', frontEndStuff)

@login_required(login_url='/admin/login/')
def commentRemove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('postDetail', pk=comment.post.pk)


@login_required(login_url='/admin/login/')
def RemovePost(request,pk):
    post_to_remove = get_object_or_404(Post, pk=pk)
    post_to_remove.delete()
    return redirect('/', pk=post_to_remove.pk)