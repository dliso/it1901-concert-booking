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
from bands import api_views

auth_urls = [
    url(r'^signup/$', acc_views.SignUpView.as_view(), name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]

stage_urls = [
    url(r'^$', band_views.StageList.as_view(), name='stagelist'),
    url(r'^(?P<stage_pk>[0-9]+)/economy/$',
        band_views.StageEconReport.as_view(), name='econreport'),
    url(r'^(?P<pk>[0-9]+)/$', band_views.StageDetail.as_view(), name='detail'),
]


concert_urls = [
    url(r'^$', band_views.ConcertList.as_view(), name='list'),
    url(r'^report/$', band_views.ConcertReport.as_view(), name='report'),
    url(r'^create/$', band_views.ConcertCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)$', band_views.ConcertDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', band_views.ConcertEdit.as_view(), name='edit'),
    url(r'^(?P<pk>[0-9]+)/edit_tech$', band_views.ConcertEditTech.as_view(), name='edit_tech'),
    url(r'^technician$', band_views.TechnicianList.as_view(), name='technicianList'),
]

band_urls = [
    url(r'^(?P<pk>[0-9]+)$', band_views.BandDetail.as_view(), name='detail'),
    url(r'^$', band_views.BandList.as_view(), name='list')
]


genre_urls = [
    url(r'^$', band_views.GenreList.as_view(), name='genrelist'),
]


festival_urls = [
    url(r'^$', band_views.FestivalList.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)$', band_views.FestivalDetail.as_view(),
        name='detail'),
]


offer_urls = [
    url(r'^$', band_views.OfferList.as_view(), name='offerList'),
    url(r'^(?P<pk>[0-9]+)$', band_views.OfferDetail.as_view(), name='offerDetail'),
    url(r'^manager$', band_views.OfferManagerList.as_view(), name='offerManagerView'),
    url(r'^manager(?P<pk>[0-9]+)$', band_views.OfferManagerDetail.as_view(), name='offerManagerDetail'),
    url(r'^new$', band_views.OfferView.as_view(), name='new'),
]


dashboard_urls = [
    url(r'^bookingdashboard/$', band_views.BookingDashboard.as_view(),
        name='booking'),
]


api_urls = [
    url(r'^occurrences/$', api_views.occurrences,
        name='occurrences'),
]


urlpatterns = [
    url(r'^search_band/$', band_views.BandSearch.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(auth_urls, namespace='auth')),
    url(r'^stages/', include(stage_urls, namespace='stages')),
    url(r'^genres/', include(genre_urls, namespace='genres')),
    url(r'^$', acc_views.Dashboard.as_view()),
    url(r'^concert/', include(concert_urls, namespace='concert')),
    url(r'^festival/', include(festival_urls, namespace='festival')),
    url(r'^offer/', include(offer_urls, namespace='offer')),
    url(r'^band/', include(band_urls, namespace='band')),
    url(r'', include(dashboard_urls, namespace='dashboards')),
    url(r'^schedule/', include('schedule.urls'), name='scheduler'),
    url(r'^api/', include(api_urls, namespace='api')),
]
