# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^$', views.FilaChamadosIndexView.as_view(), name='index'),
	url(r'^api/chamados_usuario/(?P<usuario_id>[0-9]+)/(?P<status>[\w\-]+)/$', views.chamados_usuario_json, name='api-chamados-usuario'),
	url(r'^api/chamados_abertos/(?P<setor_id>[0-9]+)/$', views.chamados_abertos_json, name='api-chamados-abertos'),
	url(r'^api/chamados_estatistica/$', views.chamados_estatistica_json, name='api-chamados-estatistica'),
]

