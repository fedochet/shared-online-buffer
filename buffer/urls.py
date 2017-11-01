from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read$', views.read, name='read'),
    url(r'^edit$', views.edit, name='edit'),
]
