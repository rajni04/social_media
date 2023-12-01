# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth import authenticate, login,logout
# from django.shortcuts import render,redirect

# # Create your views here.


# def register(request):
#     if request.method=='POST':
#         username=request.POST.get("username")
#         email=request.POST.get('email')
#         password1=request.POST.get('password1')
#         password2=request.POST.get('password2')


#         if password1==password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'USERNAME TAKEN')
#                 return redirect('register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,'EMAIL TAKEN')
#                 return HttpResponseRedirect(reverse('register'))

#             else:
#                 user=User.objects.create_user(username=username,email=email,password=password1,user_type=3)
#                 user.save();
#                 print('user created')
#                 return redirect('login')
#         else:
#             print('password mot matching')
#             return redirect('/')

#     return render(request,'logn/register.html')



# def user_login(request):
#     if request.method=="POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')

#         else:
#             messages.warning(request,'Invalid credentials')
#             return redirect('login')
#     return render(request,'login.html')

# def user_logout(request):
#     logout(request)
#     return redirect('/')

