"""concert_booker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts import views as acc_views
from bands import views as band_views

auth_urls = [
    url(r'^signup/$', acc_views.SignUpView.as_view(), name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]

stage_urls = [
    url(r'^$', band_views.StageList.as_view(), name='stagelist'),
    # url(r'^(?P<pk>[0-9]+)/$', band_views.StageList.as_view(), name='stagelist'),
]


concert_urls = [
    url(r'^$', band_views.ConcertList.as_view(), name='concertList'),
    url(r'^(?P<pk>[0-9]+)$', band_views.ConcertDetail.as_view(), name='detail'),
    url(r'^technician$', band_views.TechnicianList.as_view(), name='technicianList'),
]


genre_urls = [
    url(r'^$', band_views.GenreList.as_view(), name='genrelist'),
]


festival_urls = [
    url(r'^$', band_views.FestivalList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)$', band_views.FestivalDetail.as_view(),
        name='detail'),
]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(auth_urls, namespace='auth')),
    url(r'^stages/', include(stage_urls, namespace='stages')),
    url(r'^genres/', include(genre_urls, namespace='genres')),
    url(r'^$', acc_views.Dashboard.as_view()),
    url(r'^concert/', include(concert_urls, namespace='concert')),
    url(r'^festival/', include(festival_urls, namespace='festival')),
]
