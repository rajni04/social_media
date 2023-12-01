from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return redirect('/blog/blog')
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/blog/blog')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

# def logout_view(request):
#     print("1")
#     logout(request)
#     return redirect('/login')