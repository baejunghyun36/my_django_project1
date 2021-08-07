from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
from .models import Comment, Post
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)