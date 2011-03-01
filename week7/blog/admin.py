from django.contrib import admin
from blog.models import Blog

class AdminBlog(admin.ModelAdmin):
    pass

admin.site.register(Blog, AdminBlog)