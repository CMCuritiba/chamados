# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.CadastroChamadosIndexView.as_view(template_name='core/index.html'), name='index'),
    url(r'^api/grupo_servico/(?P<id_setor>[0-9]+)/$', views.grupo_servico_json, name='api-grupo_servico_json'),
    url(r'^api/servico/(?P<id_gs>[0-9]+)/$', views.servico_json, name='api-servico_json'),
    url(r'^api/chamados_usuario/(?P<usuario_id>[0-9]+)/$', views.chamados_usuario_json, name='api-chamados_usuario_json'),
    url(r'^(?P<id>[-\w]+)/$', views.ChamadoDetailView.as_view(template_name='core/chamado_detail.html'), name='detalhe-chamado'),
    url(r'^edita/(?P<pk>[0-9]+)/$', views.ConsolidadoChamadoDetailView.as_view(template_name='core/edit.html'), name='chamado-update'),
]

