"""
URL configuration for django_auth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .swagger import schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.jwt_auth.urls')),
    path('api/v1/', include('apps.api_getaway.urls')),
    path('profile/', include('apps.profiles.urls')),
    path('locations/', include('apps.locations.urls')),
    path('constructor/', include('apps.constructor.api.urls')),
    path('filehandler/', include('apps.filehandler.urls')),
    path('document/', include('apps.documents.urls')),
    path('news/', include('apps.news.urls')),
    path('history/', include('apps.history.urls')),
    path('report/', include('apps.report_manager.urls')),
    path('ppmi_report/', include('apps.ppmi_report.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('comment/', include('apps.comments.urls')),
    path('meeting/', include('apps.meeting.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
