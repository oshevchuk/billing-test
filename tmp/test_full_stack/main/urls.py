from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r"^scanner/(?P<id>[0-9]+)/$", scanner_read, name="scanner_read"),
    url(r'^scanner/create/$', scanner_create, name="scanner_create"),
    url(r'^scanner/(?P<id>[0-9]+)/update/$', scanner_update, name="scanner_update"),

    url(r"^connector/(?P<id>[0-9]+)/$", connector_read, name="connector_read"),
    url(r'^connector/create/$', connector_create, name="connector_create"),
    url(r'^connector/(?P<id>[0-9]+)/update/$', connector_update, name="connector_update"),
]
