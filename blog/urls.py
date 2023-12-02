from django.urls import path, include
from blog.views import (
    blog, blog_detail,share_post,search,likeBlog,
    addBlog,updateBlog,delete_post,profile_list,profile,
    user_blog)

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path("blog", blog, name="blog"),
    path("addblog", addBlog, name="addBlog"),
    path("updateBlog/<str:pk>", updateBlog, name="updateBlog"),
    path("delete_post/<str:pk>", delete_post,name="delete_post"),
    path('like/<str:pk>',likeBlog,name='like'),
    path("blog_detail/<int:pk>/", blog_detail, name="blog_detail"),
    path("share_post/<int:id>/", share_post, name="share_post"),
    path('search/', search, name='search'),
    path('profile_list/', profile_list, name='profile_list'),
    path('user_blog/',user_blog,name='user_blog'),
    path('profile/<int:pk>/', profile, name='profile'),
]