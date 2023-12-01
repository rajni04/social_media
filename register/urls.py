from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign_up'),
    path('', views.home, name="home"),

    #path('logout', views.logout_view, name='logout'),


    ]