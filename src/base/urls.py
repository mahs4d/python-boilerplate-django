from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # project app urls
    path('', include('apps.core.urls')),
    path('', include('apps.auth.urls')),
    path('', include('apps.user.urls')),
]
