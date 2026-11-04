from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at")
    search_fields = ("author__username", "caption")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")

admin.site.register(Like)
admin.site.register(Follow)
