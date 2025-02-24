"""
URL configuration for rz_autos project.

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
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from django.views.generic.base import RedirectView


admin.site.site_header = "RZ Autos"
admin.site.site_title = "RZ Autos"
admin.site.index_title = "Welcome to RZ Autos Portal"



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/web/', include('web.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/client/', include('client.urls')),

    path('', RedirectView.as_view(url='/admin/', permanent=False)),


    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
