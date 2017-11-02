from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read/([a-zA-Z0-9]{6})$', views.read, name='read'),
    url(r'^edit/([a-zA-Z0-9]{8})$', views.edit, name='edit'),
    url(r'^new$', views.new, name='new')
]
