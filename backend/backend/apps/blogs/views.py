from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Blog

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})