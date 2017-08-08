# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.core import serializers
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.views.generic import TemplateView
import datetime
from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.http import JsonResponse
from django.db import transaction

from .forms import ChamadoForm
from .models import GrupoServico, Servico, Chamado, FilaChamados, ChamadoResposta, HistoricoChamados
from autentica.util.mixin import CMCLoginRequired
from .forms import ChamadoForm

from ..lib.mail import envia_email



class ChamadoDetailView(DetailView):
    model = Chamado


class CadastroChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, FormView):
    template_name = 'core/index.html'
    form_class = ChamadoForm

#--------------------------------------------------------------------------------------
class CadastroChamadosCreateView(CMCLoginRequired, SuccessMessageMixin, CreateView):
    template_name = "core/new.html"
    form_class = ChamadoForm
    model = Chamado
    success_url = '/chamado/'
    success_message = "Chamado criado com sucesso"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.usuario = self.request.user
        obj.save()
        return super(CadastroChamadosCreateView, self).form_valid(form)

#--------------------------------------------------------------------------------------
# Retorna JSON lista de chamados do usuario
#--------------------------------------------------------------------------------------
def chamados_atendente_json(request,usuario_id, status):
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
        chamado_json['chamado_data_abertura'] = c.chamado.data_abertura.strftime("%d/%m/%Y")
        chamado_json['chamado_grupo_servico'] = c.chamado.grupo_servico.descricao
        chamado_json['chamado_servico'] = c.chamado.servico.descricao
        chamado_json['chamado_assunto'] = c.chamado.assunto
        chamado_json['chamado_usuario'] = c.chamado.usuario.username

        resposta.append(chamado_json)

    return JsonResponse(resposta, safe=False)       


#--------------------------------------------------------------------------------------
# Retorna JSON lista de chamados abertos do setor
# --------------------------------------------------------------------------------------
def chamados_abertos_json(request, setor_id):
    resposta = []

    if setor_id == None or setor_id == '' or setor_id == '0':
        chamados = None
    else:
        chamados = Chamado.objects.filter(setor__setor_id=setor_id)

    for c in chamados:
        chamado_json = {}
        chamado_json['chamado_id'] = c.id
        chamado_json['chamado_data_abertura'] = c.data_abertura.strftime("%d/%m/%Y")
        chamado_json['chamado_grupo_servico'] = c.grupo_servico.descricao
        chamado_json['chamado_servico'] = c.servico.descricao
        chamado_json['chamado_assunto'] = c.assunto
        chamado_json['chamado_usuario'] = c.usuario.username
        chamado_json['status'] = c.status

        resposta.append(chamado_json)
    
    return JsonResponse(resposta, safe=False)           

#--------------------------------------------------------------------------------------
# Retorna JSON estatistica chamados
# --------------------------------------------------------------------------------------
def chamados_estatistica_json(request):
    resposta = []

    atendidos = Chamado.objects.filter(setor__setor_id=request.session['setor_id']).filter(status='FECHADO').count()
    abertos = Chamado.objects.filter(setor__setor_id=request.session['setor_id']).filter(status='ABERTO').count()
    atendimento = Chamado.objects.filter(setor__setor_id=request.session['setor_id']).filter(status='ATENDIMENTO').count()

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

# --------------------------------------------------------------------------------------
class FilaChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, TemplateView):
    template_name = 'fila/index.html'


# --------------------------------------------------------------------------------------
# Retorna JSON dos grupos de serviços para setor especificado
# --------------------------------------------------------------------------------------
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


# --------------------------------------------------------------------------------------
# Retorna JSON dos serviços para o grupo de serviço especificado
# --------------------------------------------------------------------------------------
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
        chamado_json['chamado_id'] = c.id
        chamado_json['data_abertura'] = c.data_abertura.strftime("%d/%m/%Y")
        chamado_json['grupo_servico'] = c.grupo_servico.descricao
        chamado_json['setor'] = c.setor.setor.set_nome
        chamado_json['servico'] = c.servico.descricao
        chamado_json['assunto'] = c.assunto
        chamado_json['status'] = c.status
        chamado_json['novidade'] = c.novidade

        resposta.append(chamado_json)

    return JsonResponse(resposta, safe=False)

#--------------------------------------------------------------------------------------
# Quando um atendente seleciona um chamado para atender
#--------------------------------------------------------------------------------------
def atende(request):
    if request.method =='POST':
        id_chamado = request.POST.get('id_chamado')

        if id_chamado != None and id_chamado != '':
            chamado = Chamado.objects.get(pk=id_chamado)
            if chamado.status != 'ABERTO':
                raise ValueError('Chamado selecionado por outro atendente.')
            FilaChamados.objects.atende(request.user, chamado)
    return HttpResponseRedirect('/fila/')

#--------------------------------------------------------------------------------------
# Quando um atendente devolve um chamado
#--------------------------------------------------------------------------------------
def devolve(request):
    if request.method =='POST':
        id_chamado = request.POST.get('id_chamado')

        if id_chamado != None and id_chamado != '':
            chamado = Chamado.objects.get(pk=id_chamado)
            FilaChamados.objects.devolve(request.user, chamado)
    return HttpResponseRedirect('/fila/')    

#--------------------------------------------------------------------------------------
# Quando um atendente seleciona um chamado para atender
#--------------------------------------------------------------------------------------
def atende_json(request, id_chamado):
    if id_chamado != None and id_chamado != '':
        chamado = Chamado.objects.get(pk=id_chamado)
        if chamado.status != 'ABERTO':
            response = JsonResponse({'status':'false','message':'Chamado selecionado por outro atendente'}, status=401)
        FilaChamados.objects.atende(request.user, chamado)
        response = JsonResponse({'status':'true','message':'Chamado selecionado com sucesso'}, status=200)
    else:
        response = JsonResponse({'status':'false','message':'Nenhum chamado selecionado'}, status=401)
    return response

#--------------------------------------------------------------------------------------
# Quando um atendente devolve um chamado
#--------------------------------------------------------------------------------------
def devolve_json(request, id_chamado):
    if id_chamado != None and id_chamado != '':
        chamado = Chamado.objects.get(pk=id_chamado)
        FilaChamados.objects.devolve(request.user, chamado)
        response = JsonResponse({'status':'true','message':'Chamado devolvido com sucesso'}, status=200)
    else:
        response = JsonResponse({'status':'false','message':'Nenhum chamado selecionado'}, status=401)
    return response

#--------------------------------------------------------------------------------------
class ConsolidadoChamadoDetailView(CMCLoginRequired, SuccessMessageMixin, DetailView):
    template_name = "core/edit.html"
    model = Chamado
    success_url = '/fila/'
    success_message = "Chamado atualizadao com sucesso"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        chamado = Chamado.objects.get(pk=self.get_object().id)
        if self.template_name == "core/detail.html":
            chamado.novidade = False
            chamado.save()
        fila = FilaChamados.objects.get(chamado=chamado)
        #respostas = ChamadoResposta.objects.filter(chamado=self.get_object().id)
        #context['respostas'] = respostas
        context['atendente'] = fila.usuario
        return context

#--------------------------------------------------------------------------------------
# Retorna JSON lista de respostas chamado
#--------------------------------------------------------------------------------------
def respostas_json(request, id_chamado):
    resposta = []

    if id_chamado == None or id_chamado == '' or id_chamado == '0':
        respostas = None
    else:
        respostas = ChamadoResposta.objects.filter(chamado_id=id_chamado)

    for r in respostas:
        resposta_json = {}
        resposta_json['resposta_id'] = r.id
        resposta_json['chamado_id'] = r.chamado.id
        resposta_json['data'] = r.data.strftime("%d/%m/%Y %H:%M")
        resposta_json['usuario'] = r.usuario.username
        resposta_json['resposta'] = r.resposta
        
        resposta.append(resposta_json)

    return JsonResponse(resposta, safe=False)        

#--------------------------------------------------------------------------------------
# Salva uma resposta
#--------------------------------------------------------------------------------------
def responde_json(request):

    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('id_chamado') != None and request.POST.get('id_chamado') != '':
            chamado = Chamado.objects.get(pk=request.POST.get('id_chamado'))
            chamado.novidade = True 
            chamado.save()
            if request.POST.get('resposta_id') != None and request.POST.get('resposta_id') != '':
                cresposta = ChamadoResposta.objects.get(pk=request.POST.get('resposta_id'))
                cresposta.resposta = request.POST.get('resposta')
                cresposta.save()
            else:
                ChamadoResposta.objects.create(usuario=request.user, chamado=chamado, resposta=request.POST.get('resposta'))
            envia_email(chamado)
            response = JsonResponse({'status':'true','message':'Chamado selecionado com sucesso'}, status=200)
        else:
            response = JsonResponse({'status':'false','message':'Chamado inválido'}, status=401)
    else:
        response = JsonResponse({'status':'false','message':'Nenhum chamado selecionado'}, status=401)
    return response    

#--------------------------------------------------------------------------------------
# Fecha o chamado
#--------------------------------------------------------------------------------------
@transaction.atomic
def fecha(request):

    if request.method == 'POST':
        if request.POST.get('id_chamado') != None and request.POST.get('id_chamado') != '':
            chamado = Chamado.objects.get(pk=request.POST.get('id_chamado'))
            chamado.status = 'FECHADO'
            chamado.save()

            historico = HistoricoChamados.objects.create(chamado=chamado, status='FECHADO')
            historico.save()
        else:
            raise ValueError('Chamado inválido.')
    return HttpResponseRedirect('/fila/')
