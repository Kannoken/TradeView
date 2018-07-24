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
from TradeViewApp.views import main, servers_list, server_detail, server_symbols
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'', main),
    url(r'^servers/$',servers_list, name='server-list'),
    url(r'^servers/(?P<pk>[0-9]+)/$', server_detail),
    url(r'^symbols/', server_symbols),
    # url(r'^servers$', get_by_id, name='server-list'),
    # # url(r'^servers/$', ServerList.as_view(), name='server-list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
