# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^servico/$', views.ServicoIndexView.as_view(), name='cadastro-servico'),
    url(r'^servico/new/$', views.ServicoCreateView.as_view(), name='cadastro-servico-new'),
    url(r'^servico/edit/(?P<pk>[0-9]+)/$', views.ServicoUpdateView.as_view(), name='cadastro-servico-update'),
    url(r'^api/servico/delete/(?P<pk>[0-9]+)/$', views.exclui_servico_json, name='api-exclui-servico-json'),

    url(r'^grupo_servico/$', views.GrupoServicoIndexView.as_view(), name='cadastro-grupo-servico'),
    url(r'^grupo_servico/new/$', views.GrupoServicoCreateView.as_view(), name='cadastro-grupo-servico-new'),
    url(r'^grupo_servico/edit/(?P<pk>[0-9]+)/$', views.GrupoServicoUpdateView.as_view(), name='cadastro-grupo-servico-update'),
    url(r'^api/grupo_servico/delete/(?P<pk>[0-9]+)/$', views.exclui_grupo_servico_json, name='api-exclui-grupo-servico-json'),

    url(r'^setor/$', views.SetorChamadoIndexView.as_view(), name='cadastro-setor'),
    url(r'^setor/new/$', views.SetorChamadoCreateView.as_view(), name='cadastro-setor-new'),
]

