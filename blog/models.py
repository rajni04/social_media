from django.db import models
from tinymce.models import HTMLField
from django.utils.html import format_html

from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    follow=models.ManyToManyField("self", related_name='followed_by',symmetrical=False,blank=True)
    bio=models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=250)

    def __str__(self):
        return self.title
class Blog(models.Model):
    title=models.CharField(max_length=1000)
    content=HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image=models.ImageField(upload_to="post/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes=models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])
    def image_tag(self):
        return format_html('<img src="/media/{}" style="width:40px;heiht:40px"/>'.format(self.image))

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='post')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    likes=models.IntegerField(default=0)
    #categories = models.ManyToManyField("Category", related_name="category")

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now_add=True)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> {self.followed}"




