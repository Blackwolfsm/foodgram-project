from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    import debug_toolbar

urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)