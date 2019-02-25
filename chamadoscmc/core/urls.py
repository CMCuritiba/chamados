# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.CadastroChamadosIndexView.as_view(template_name='core/index.html'), name='index'),
    url(r'^api/grupo_servico/(?P<id_setor>[0-9]+)/$', views.grupo_servico_json, name='api-grupo_servico_json'),
    url(r'^api/grupo_servico_todos/(?P<id_setor>[0-9]+)/$', views.grupo_servico_todos_json, name='api-grupo_servico_todos_json'),
    url(r'^api/servico/(?P<id_gs>[0-9]+)/$', views.servico_json, name='api-servico_json'),
    url(r'^api/servico_todos/(?P<setor_id>[0-9]+)/$', views.servico_todos_json, name='api-servico_todos_json'),
    url(r'^api/patrimonio/(?P<id_gs>[0-9]+)/$', views.patrimonio_servico_json, name='api-patrimonio_json'),
    url(r'^api/chamados_usuario/(?P<usuario_id>[0-9]+)/$', views.chamados_usuario_json, name='api-chamados_usuario_json'),
    url(r'^api/localizacao/$', views.localizacao_json, name='api-localizacao_json'),
    url(r'^api/pavimento/(?P<id_localizacao>[0-9]+)/$', views.pavimentos_json, name='api-pavimentos_json'),
    url(r'^api/localizacao_setor/(?P<id_setor>[0-9]+)/$', views.localizacao_setor_json, name='api-localizacao_setor_json'),
    url(r'^api/setores/$', views.setores_json, name='api-setores_json'),
    #url(r'^(?P<id>[-\w]+)/$', views.ChamadoDetailView.as_view(template_name='core/chamado_detail.html'), name='detalhe-chamado'),
    url(r'^edita/(?P<pk>[0-9]+)/$', views.ConsolidadoChamadoEditlView.as_view(template_name='core/edit.html'), name='chamado-update'),
    url(r'^detalhe/(?P<pk>[0-9]+)/$', views.ConsolidadoChamadoDetailView.as_view(template_name='core/detail.html'), name='chamado-detalhe'),
    url(r'^cria/$', views.CadastroChamadosCreateView.as_view(), name='cria'),
    #url(r'^relatorio/$', views.relatorio, name='relatorio'),
    url(r'^relatorio/$', views.RelatorioChamados.as_view(), name='relatorio'),
    url(r'^imprime/$', views.ImprimeChamado.as_view(), name='imprime'),
]

