from django.contrib import admin
from .models import Blog, Comment, Profile, Follow
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ("image_tag","title", "author")
    search_fields=('title',)
admin.site.register(Blog, BlogAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_post', 'registered_user']
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Follow)


