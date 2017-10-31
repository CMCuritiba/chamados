# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^servico/$', views.ServicoIndexView.as_view(), name='cadastro-servico'),
    url(r'^servico/new/$', views.ServicoCreateView.as_view(), name='cadastro-servico-new'),
    url(r'^servico/edit/(?P<pk>[0-9]+)/$', views.ServicoUpdateView.as_view(), name='cadastro-servico-update'),
    url(r'^api/servico/delete/(?P<pk>[0-9]+)/$', views.exclui_servico_json, name='api-exclui-servico-json'),
]

