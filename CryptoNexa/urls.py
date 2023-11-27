"""
URL configuration for CryptoNexa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from CryptoNexa import views, settings

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', views.index, name='index'),
  path('', include('core.urls')),
  path('', include('Newsletter.urls')),
  path('', include('ContactUS.urls')),
  path('currencyExchange/', include('currencyExchange.urls')),
  path('', include('payments.urls')),
  path('', include('BuySell.urls')),
  path('', include('portfolio.urls')),
  path('', include('support.urls')),
  path('filter_crypto_data', views.filter_crypto_data, name='filter_crypto_data'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)