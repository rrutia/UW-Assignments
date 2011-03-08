from django.shortcuts import render_to_response
from blog.models import Blog

def index(request):
    entries = Blog.objects.all().order_by('-date')
    return render_to_response('index.html', locals())

def about(request):
    return render_to_response('about.html', locals())
