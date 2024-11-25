"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.conf.urls.static import static

from webapp import settings

# URL patterns dasar tanpa prefix bahasa
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('account.urls')),
    path("", include('booking.urls')),
    path("", include('course.urls')),
    path('set-language/', set_language, name='set_language'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URL patterns dengan prefix bahasa (i18n)
urlpatterns += i18n_patterns(
    path("", include('account.urls')),
    path("", include('booking.urls')), # Mengharuskan prefix bahasa di semua URL
    path("", include('course.urls'))
)