from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm

def community_home(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    posts = Post.objects.all().order_by('-created_at')
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('community_home')
        else:
            form = PostForm() 
    else:
        form = None  

    posts = Post.objects.all().order_by("-created_at")
    return render(request, "community_app/community_home.html", {"posts": posts,'profile':profile,'form':form})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("community_home")
    else:
        form = PostForm()
    return render(request, "community_app/create_post.html", {"form": form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(request, "community_app/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
    })
