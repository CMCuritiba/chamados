# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.shortcuts import render_to_response
import json
from django.core import serializers
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.views.generic import TemplateView
import datetime

from ..autentica.util.mixin import CMCLoginRequired
from .forms import ChamadoForm

from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView
from ..autentica.util.mixin import CMCLoginRequired
from .forms import ChamadoForm
from .models import GrupoServico, Servico, Chamado, FilaChamados
from django.http import JsonResponse


class ChamadoDetailView(DetailView):
    model = Chamado


class CadastroChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, FormView):
    template_name = 'core/index.html'
    form_class = ChamadoForm


#--------------------------------------------------------------------------------------
class CadastroChamadosCreateView(CMCLoginRequired, SuccessMessageMixin, CreateView):
    template_name = "cadastro/new.html"
    form_class = ChamadoForm
	model = Chamado
	success_url = '/cadastro/'
	success_message = "Chamado criado com sucesso"

#--------------------------------------------------------------------------------------
# Retorna JSON lista de chamados do usuario
#--------------------------------------------------------------------------------------
def chamados_usuario_json(request,usuario_id, status):
	resposta = []

	if usuario_id == None or usuario_id == '' or usuario_id == '0':
		chamados = None
	else:
		chamados = FilaChamados.objects.filter(usuario_id=usuario_id)
	if status != None and status != '':
		chamados = FilaChamados.objects.filter(usuario_id=usuario_id).filter(chamado__status=status)

	for c in chamados:
		chamado_json = {}
		chamado_json['fila_id'] = c.id
		chamado_json['chamado_id'] = c.chamado.id
		chamado_json['chamado_data_abertura'] = c.chamado.data_abertura.strftime("%d/%m/%Y %H:%M")
		chamado_json['chamado_grupo_servico'] = c.chamado.grupo_servico.descricao
		chamado_json['chamado_servico'] = c.chamado.servico.descricao
		chamado_json['chamado_assunto'] = c.chamado.assunto
		chamado_json['chamado_usuario'] = c.chamado.usuario.username

		resposta.append(chamado_json)
	
	return JsonResponse(resposta, safe=False)		


#--------------------------------------------------------------------------------------
# Retorna JSON lista de chamados abertos do setor
#--------------------------------------------------------------------------------------
def chamados_abertos_json(request, setor_id):
	resposta = []

	if setor_id == None or setor_id == '' or setor_id == '0':
		chamados = None
	else:
		chamados = Chamado.objects.filter(setor__setor_id=setor_id).filter(status='ABERTO')

	for c in chamados:
		chamado_json = {}
		chamado_json['chamado_id'] = c.id
		chamado_json['chamado_data_abertura'] = c.data_abertura.strftime("%d/%m/%Y %H:%M")
		chamado_json['chamado_grupo_servico'] = c.grupo_servico.descricao
		chamado_json['chamado_servico'] = c.servico.descricao
		chamado_json['chamado_assunto'] = c.assunto
		chamado_json['chamado_usuario'] = c.usuario.username

		resposta.append(chamado_json)
	
	return JsonResponse(resposta, safe=False)			

#--------------------------------------------------------------------------------------
# Retorna JSON estatistica chamados
#--------------------------------------------------------------------------------------
def chamados_estatistica_json(request):
	resposta = []

	atendidos = FilaChamados.objects.filter(chamado__status='FECHADO').count()
	abertos = FilaChamados.objects.filter(chamado__status='ABERTO').count()
	atendimento = FilaChamados.objects.filter(chamado__status='ATENDIMENTO').count()

	oatendidos = {}
	oatendidos['atendidos'] = atendidos
	resposta.append(oatendidos)

	oabertos = {}
	oabertos['abertos'] = abertos
	resposta.append(oabertos)

	oatendimento = {}
	oatendimento['atendimento'] = atendimento
	resposta.append(oatendimento)

	return JsonResponse(resposta, safe=False)				

#--------------------------------------------------------------------------------------
class FilaChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, TemplateView):
	template_name = 'fila/index.html'	


#--------------------------------------------------------------------------------------
# Retorna JSON dos grupos de serviços para setor especificado
#--------------------------------------------------------------------------------------
def grupo_servico_json(request, id_setor):
    resposta = []

    if id_setor == None or id_setor == '' or id_setor == '0':
        grupos_servicos = None
    else:
        grupos_servicos = GrupoServico.objects.filter(setor=id_setor)

    for gs in grupos_servicos:
        grupo_servico_json = {}
        grupo_servico_json['gs_id'] = gs.id
        grupo_servico_json['gs_descricao'] = gs.descricao
        resposta.append(grupo_servico_json)

    return JsonResponse(resposta, safe=False)


#--------------------------------------------------------------------------------------
# Retorna JSON dos serviços para o grupo de serviço especificado
#--------------------------------------------------------------------------------------
def servico_json(request, id_gs):
	resposta = []

	if id_gs == None or id_gs == '' or id_gs == '0':
		servicos = None
	else:
		servicos = Servico.objects.filter(grupo_servico=id_gs)

	for s in servicos:
		servico_json = {}
		servico_json['servico_id'] = s.id
		servico_json['servico_descricao'] = s.descricao
		resposta.append(servico_json)


	return JsonResponse(resposta, safe=False)





#--------------------------------------------------------------------------------------
# Retorna JSON lista de chamados do usuario
#--------------------------------------------------------------------------------------
def chamados_usuario_json(request, usuario_id):
	resposta = []

	if usuario_id == None or usuario_id == '' or usuario_id == '0':
		chamados = None
	else:
		chamados = Chamado.objects.filter(usuario_id=usuario_id)

	for c in chamados:
		chamado_json = {}
		chamado_json['chamado_id'] = c.chamado.id
		chamado_json['chamado_data_abertura'] = c.chamado.data_abertura
		chamado_json['chamado_grupo_servico'] = c.chamado.grupo_servico.descricao
		chamado_json['chamado_servico'] = c.chamado.servico.descricao
		chamado_json['chamado_assunto'] = c.chamado.chamado_assunto

		resposta.append(chamado_json)

	return JsonResponse(resposta, safe=False)
