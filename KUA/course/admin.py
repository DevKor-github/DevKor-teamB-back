from django.contrib import admin
from .models import Course, Post, Tag, Comment

admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
