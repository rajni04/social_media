from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import *
from blog.forms import CommentForm, EmailPostForm,blogForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

def blog(request):
    blog = Blog.objects.all().order_by("-created")
    paginator = Paginator(blog, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        "blogs": page_obj,
    }
    return render(request, "blog/all_blog.html", context)

#api to like a blog
def likeBlog(request,pk):
    blog=Blog.objects.get(id=pk)
    blog.likes+=1
    blog.save()
    return redirect('/')

#create post api
@login_required(login_url="/login")
def addBlog(request):

    form=blogForm()
    if request.method=='POST':
        form=blogForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form,
    }
    return render(request,'blog/add_blog.html',context)


#edit blog
@login_required(login_url="/login")
def updateBlog(request,pk):
    try:
        blog=Blog.objects.get(id=pk)
        if blog.author !=request.user:
            return redirect('/')
        form=blogForm(instance=blog)
        if request.method=='POST':
            form=blogForm(request.POST,instance=blog)
            if form.is_valid():
                form.save()
                messages.success(request,"Successfully Updated ")
                return redirect('/')
        context={
            'form':form
        }
    except Exception as e:
        print(e)
    return render(request,'blog/edit_blog.html',context)
@login_required(login_url="/login")
def delete_post(request,pk):
    blog=Blog.objects.get(id=pk)
    blog.delete()
    return redirect('/')


@login_required(login_url="/login")
def blog_detail(request, pk):
    post = Blog.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    #comments = Comment.objects.filter(blog=blog_post)
    comments = Comment.objects.filter(post=post)
    print("comments",comments)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)

def profile_list(request):
    if request.user.is_authenticated:
        profiles=Profile.objects.exclude(user=request.user)
        context = {
        "profiles": profiles
        }
        return render(request, 'blog/profile_list.html',context)
    else:
        return redirect('/')
@login_required(login_url="/login")
def share_post(request, id):
    post = Blog.objects.get(id=id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends that you read {post.title}"
            message = f"Read this post I found on Galaxy. The url is {post_url} and the title is {post.title}. {cd['name']} gave the comment below {cd['comments']}"

            send_mail(
                subject=subject,
                message=message,
                from_email=request.user.email,
                recipient_list=[cd['to']]
            )

            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,
                                                    'form': form,
                                                    'sent':sent})
def search(request):
    search_blog=request.GET.get('search')
    if search_blog:
        blogs= Blog.objects.filter(Q(title__icontains=search_blog)|Q(author__username__icontains=search_blog))
    else:
        messages.warning(request, "No search results found. Please refine your query.")
    return render(request, 'blog/search.html', {'blogs':blogs})
def follow_unfollow_user(request):
    if request.method=='POST':
        my_profile = Profile.objects.get(user=request.user)
        profile_pk=request.POST.get('profile_pk')
        print(f"ddd--{profile_pk}----")
        obj=Profile.objects.get(pk=profile_pk)
        print("obj--",obj)
        if obj.user in my_profile.follow.all():
            my_profile.follow.remove(obj.user)
        else:
            my_profile.follow.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('blog/profile_list.html')

#@login_required(login_url='/loginn')
def user_blog(request):
    blogs = Blog.objects.filter(author=request.user)
    print("blog",blogs)
    context={
        'blogs':blogs
    }
    return render(request, 'blog/user_blog_filter.html',context)


