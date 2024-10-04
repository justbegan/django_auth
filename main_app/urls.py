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
    path('profile_manager/', include('apps.profiles_manager.urls')),
    path('locations/', include('apps.locations.urls')),
    path('constructor/', include('apps.constructor.urls')),
    path('filehandler/', include('apps.filehandler.urls')),
    path('document/', include('apps.documents.urls')),
    path('news/', include('apps.news.urls')),
    path('history/', include('apps.history.urls')),
    path('report/', include('apps.report_manager.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('comment/', include('apps.comments.urls')),
    path('faq/', include('apps.faq.urls')),
    path('phone_book/', include('apps.phone_book.urls')),
    path('ppmi_report/', include('apps_modules.ppmi_report.urls')),
    path('meeting/', include('apps_modules.meeting.urls')),
    path('letter/', include('apps_modules.letter.urls')),
    path('module_manager/', include('apps.module_manager.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
