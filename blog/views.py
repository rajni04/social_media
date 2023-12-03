from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import *
from blog.forms import CommentForm, EmailPostForm,blogForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
# Get an instance of a logger
# Create your views here.
def blog(request):
    '''Pagination to show only 5 post'''
    blog = Blog.objects.all().order_by("-created")
    paginator = Paginator(blog, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "blogs": page_obj,
    }
    return render(request, "blog/all_blog.html", context)

def likeBlog(request,pk):
    '''Implementation of like functionality'''
    blog=Blog.objects.get(id=pk)
    blog.likes+=1
    blog.save()
    return redirect('/')

@login_required(login_url="/login")
def addBlog(request):
    '''Create blog'''
    form=blogForm()
    if request.method=='POST':
        author=request.user
        form=blogForm(request.POST,request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.author=request.user
            blog.save()

            return redirect('/')
    context={
        'form':form,
    }
    return render(request,'blog/add_blog.html',context)

@login_required(login_url="/login")
def updateBlog(request,pk):
    '''Edit blog'''
    try:
        blog=Blog.objects.get(id=pk)
        if blog.author !=request.user:
            return redirect('/')
        form=blogForm(instance=blog)
        if request.method=='POST':
            form=blogForm(request.POST,instance=blog)
            if form.is_valid():
                form.save()
                return redirect(request.META.get("HTTP_REFERER"))

        context={
            'form':form
        }
    except Exception as e:
        print(e)
    return render(request,'blog/edit_blog.html',context)

@login_required(login_url="/login")
def delete_post(request,pk):
    '''Delete blog'''
    blog=Blog.objects.get(id=pk)
    blog.delete()
    return redirect('/')

@login_required(login_url="/login")
def blog_detail(request, pk):
    '''Comment functionality Implemented'''
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
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)

def profile_list(request):
    '''Get all users except the login user'''
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
    '''Share post using email'''
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
@login_required(login_url="/login")
def profile(request, pk):
    '''Follow and unfollow '''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        blog=Blog.objects.filter(author=profile.user)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follow.remove(profile)
            elif action == "follow":
                current_user_profile.follow.add(profile)
            current_user_profile.save()
        return render(request, "blog/profile.html", {"profile":profile,"blogs":blog})
    else:
        return redirect(request.META.get("HTTP_REFERER"))

@login_required(login_url='/login')
def user_blog(request):
    blogs = Blog.objects.filter(author=request.user)
    context={
        'blogs':blogs
    }
    return render(request, 'blog/user_blog_filter.html',context)
def search(request):
    '''Search blog by using title or usernam'''
    search_blog=request.GET.get('search')
    if search_blog:
        blogs= Blog.objects.filter(Q(title__icontains=search_blog)|Q(author__username__icontains=search_blog))
    else:
        return render(request, 'blog/search.html', {'blogs':blogs})


