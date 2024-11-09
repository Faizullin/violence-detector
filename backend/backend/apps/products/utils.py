from django.core.cache import cache


def get_filters_cache():
    cache_key = "cache_filters_api_key"
    return cache_key, cache, cache.get(cache_key)
