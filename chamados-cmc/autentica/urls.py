# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^loga/$', views.loga, name='loga'),
	url(r'^sair/$', views.sair, name='sair'),
	url(r'^valida-usuario/$', views.valida_usuario, name='valida-usuario'),
]

