from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.admin_dashboard.admin import CustomAdminSite

admin.site.__class__ = CustomAdminSite

urlpatterns = [
    path('dd/admin/', admin.site.urls),
    path('', include('apps.admin_dashboard.urls', namespace='admin_dashboard')),
    path('', include('apps.accounts.urls', namespace='accounts')),
    path('', include('apps.devices.urls', namespace='devices')),
    path('', include('apps.violence_detection.urls', namespace='violence_detection')),
    path('', include('apps.pages.urls', namespace='pages')),
    path('', include('apps.blogs.urls', namespace='blogs')),
    # path('', include('apps.products.urls', namespace='products')),
    # path('', include('apps.contact_us.urls', namespace='contact_us')),
    # path('', include('app.cart.urls')),
    # path('checkout/', include('checkout.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
                      *urlpatterns,
                  ] + debug_toolbar_urls()
