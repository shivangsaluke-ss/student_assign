"""
<<<<<<< HEAD
URL configuration for sams_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
=======
URL configuration for sams_project project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('sams_app.urls')),
]

<<<<<<< HEAD
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'sams_app.views.error_403'
handler404 = 'sams_app.views.error_404'
handler500 = 'sams_app.views.error_500'
=======
# Static & Media serving fallback for production/container environments
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
