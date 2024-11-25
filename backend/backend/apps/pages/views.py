from apps.blogs.models import Blog
from django.core.cache import cache
from django.shortcuts import render


def home(request):
    cache_key = 'homepage_blogs'
    homepage_blogs = cache.get(cache_key, None)
    if homepage_blogs is None:
        homepage_blogs = list(Blog.objects.select_related(
            'author').filter(is_featured=True).order_by('created_at'))
        cache.set(cache_key, homepage_blogs, timeout=3600)  # 1 hour
    return render(request, "home/home.html", {
        'blogs': homepage_blogs
    })
