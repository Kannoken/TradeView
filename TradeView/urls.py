"""TradeView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import  url, include
from TradeViewApp.views import main, servers_list, server_detail, server_symbols, server_symbols_data
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', main),
    url(r'^api/v1/servers/$',servers_list, name='server-list'),
    url(r'^api/v1/servers/(?P<pk>[0-9]+)/$', server_detail),
    url(r'^api/v1/symbols/$', server_symbols),
    url(r'^api/v1/symbols/(?P<symbol>[-\w]+)/$', server_symbols),
    url(r'^api/v1/symbols/(?P<symbol>[-\w]+)/fields=(?P<fields>[-\w,]+)/$',server_symbols_data),
    url('^admin/', admin.site.urls),

]
