from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('products/', include('apps.products.urls')),
    path('users/', include('apps.users.urls')),
    path('contacts/', include('apps.contacts.urls')),
    path('cart/', include('apps.carts.urls')),
    path('', include('apps.common.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()

# from Adeploy:
# if settings.DEBUG:
#     from django.conf.urls.static import static
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#
#     # Serve static and media files from development server
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# todo Question: Why include static and media urls only in Debug=True
