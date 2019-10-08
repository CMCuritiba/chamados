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
from django.utils.timezone import datetime
from datetime import timedelta
from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.http import JsonResponse
from django.db import transaction
from django import forms
from django.forms.utils import ErrorList
from django.db.models import Q
from django.shortcuts import render
from django.conf import settings

import datetime

from .forms import ChamadoForm
from .models import GrupoServico, Servico, Chamado, FilaChamados, ChamadoResposta, HistoricoChamados, SetorChamado, Localizacao, Pavimento, ChamadoAnexo
from .models import ChamadoAssinatura, ChamadoReaberto
from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired
from .forms import ChamadoForm, ServicoSearchForm, ServicoForm, GrupoServicoForm, RelatorioSetorForm, SetorChamadoForm

from ..lib.fila import FilaManager
from ..lib.mixin import ChamadosAdminRequired, ChamadosAtendenteRequired, ChamadosVisualizaRequired

from templated_docs import fill_template
from templated_docs.http import FileResponse

from consumer.lib.helper import ServiceHelper
from consumer.lib.msconsumer import MSCMCConsumer

from cmcreport.lib.views import CMCReportView

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class ChamadoDetailView(DetailView):
    model = Chamado

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class CadastroChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, FormView):
    template_name = 'core/index.html'
    form_class = ChamadoForm

#--------------------------------------------------------------------------------------
#
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
        obj.setor_solicitante = self.request.session['setor_id']
        obj.save()
        fila = FilaManager()
        fila.cria(self.request.user, obj)
        if self.request.FILES:
            for f in self.request.FILES.getlist('foto'):
                foto = ChamadoAnexo.objects.create(chamado=obj, arquivo=f)

        return super().form_valid(form)

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
        chamado_json['chamado_data_abertura'] = c.chamado.data_abertura
        chamado_json['chamado_grupo_servico'] = c.chamado.grupo_servico.descricao
        chamado_json['chamado_servico'] = c.chamado.servico.descricao
        chamado_json['chamado_assunto'] = c.chamado.assunto
        chamado_json['chamado_usuario'] = c.chamado.usuario.username
        chamado_json['chamado_reaberto'] = c.chamado.reaberto
        chamado_json['chamado_descricao'] = c.chamado.descricao

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
        chamados = Chamado.objects.filter(setor__setor_id=setor_id, status='ABERTO').order_by('-id')[:100]
        #chamados = Chamado.objects.filter(setor__setor_id=27)
    '''        
    if len(chamados) == 0:
        chamados = Chamado.objects.filter(setor_setor_id_superior=setor_id)
        #chamados = Chamado.objects.filter(setor__setor__set_id_superior=27)
    '''        

    for c in chamados:
        chamado_json = {}
        chamado_json['chamado_id'] = c.id
        chamado_json['chamado_data_abertura'] = c.data_abertura
        chamado_json['chamado_grupo_servico'] = c.grupo_servico.descricao
        chamado_json['chamado_servico'] = c.servico.descricao
        chamado_json['chamado_assunto'] = c.assunto
        chamado_json['chamado_usuario'] = c.usuario.username
        chamado_json['status'] = c.status
        chamado_json['reaberto'] = c.reaberto
        chamado_json['descricao'] = c.descricao.replace('/<\/?[^>]+>/gi', '')
        fila = FilaChamados.objects.filter(chamado=c.id).first()
        if fila == None or fila.usuario == None:
            chamado_json['fila_usuario'] = ''
        else:
            chamado_json['fila_usuario'] = fila.usuario.username

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

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class FilaChamadosIndexView(ChamadosAtendenteRequired, SuccessMessageMixin, TemplateView):
    template_name = 'fila/index.html'

# --------------------------------------------------------------------------------------
# Retorna JSON dos grupos de serviços para setor especificado
# --------------------------------------------------------------------------------------
def grupo_servico_json(request, id_setor):
    resposta = []

    if id_setor == None or id_setor == '' or id_setor == '0':
        grupos_servicos = None
    else:
        grupos_servicos = GrupoServico.objects.filter(setor=id_setor).order_by("descricao")

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
        servicos = Servico.objects.filter(grupo_servico=id_gs).order_by("descricao")

    for s in servicos:
        servico_json = {}
        servico_json['servico_id'] = s.id
        servico_json['servico_descricao'] = s.descricao
        resposta.append(servico_json)


    return JsonResponse(resposta, safe=False)

# --------------------------------------------------------------------------------------
# Retorna JSON dos serviços para o grupo de serviço especificado
# --------------------------------------------------------------------------------------
def servico_todos_json(request, setor_id):
    resposta = []

    if setor_id == None or setor_id == '' or setor_id == '0':
        servicos = None
    else:
        servicos = Servico.objects.filter(grupo_servico__setor__setor_id=setor_id)

    for s in servicos:
        servico_json = {}
        servico_json['servico_id'] = s.id
        servico_json['grupo_id'] = s.grupo_servico.id
        servico_json['servico_descricao'] = s.descricao
        resposta.append(servico_json)


    return JsonResponse(resposta, safe=False)    

# --------------------------------------------------------------------------------------
# Retorna JSON dos grupos de serviços para setor especificado
# --------------------------------------------------------------------------------------
def grupo_servico_todos_json(request, id_setor):
    resposta = []

    if id_setor == None or id_setor == '' or id_setor == '0':
        grupos_servicos = None
    else:
        grupos_servicos = GrupoServico.objects.filter(setor__setor_id=id_setor).order_by('descricao')

    for gs in grupos_servicos:
        grupo_servico_json = {}
        grupo_servico_json['gs_id'] = gs.id
        grupo_servico_json['gs_descricao'] = gs.descricao
        resposta.append(grupo_servico_json)

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
        chamado_json['data_abertura'] = c.data_abertura
        chamado_json['grupo_servico'] = c.grupo_servico.descricao
        chamado_json['setor'] = c.setor.get_nome()
        chamado_json['servico'] = c.servico.descricao
        chamado_json['assunto'] = c.assunto
        chamado_json['status'] = c.status
        chamado_json['novidade'] = c.novidade
        chamado_json['reaberto'] = c.reaberto

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
            fila = FilaManager()
            fila.atende(request.user, chamado)
    return HttpResponseRedirect('/fila/')

#--------------------------------------------------------------------------------------
# Quando um atendente devolve um chamado
#--------------------------------------------------------------------------------------
def devolve(request):
    if request.method =='POST':
        id_chamado = request.POST.get('id_chamado')

        if id_chamado != None and id_chamado != '':
            chamado = Chamado.objects.get(pk=id_chamado)
            fila = FilaManager()
            fila.devolve(request.user, chamado)
    return HttpResponseRedirect('/fila/')    

#--------------------------------------------------------------------------------------
# Quando um atendente seleciona um chamado para atender
#--------------------------------------------------------------------------------------
def atende_json(request, id_chamado):
    if id_chamado != None and id_chamado != '':
        chamado = Chamado.objects.get(pk=id_chamado)
        if chamado.status != 'ABERTO':
            response = JsonResponse({'status':'false','message':'Chamado selecionado por outro atendente'}, status=401)
        fila = FilaManager()
        fila.atende(request.user, chamado)
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
        fila = FilaManager()
        fila.devolve(request.user, chamado)
        response = JsonResponse({'status':'true','message':'Chamado devolvido com sucesso'}, status=200)
    else:
        response = JsonResponse({'status':'false','message':'Nenhum chamado selecionado'}, status=401)
    return response
#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class ConsolidadoChamadoDetailView(ChamadosVisualizaRequired, SuccessMessageMixin, DetailView):
    template_name = "core/detail.html"
    model = Chamado
    success_url = '/fila/'
    success_message = "Chamado atualizadao com sucesso"

    def get_context_data(self, **kwargs):
        s_helper = ServiceHelper()

        context = super(DetailView, self).get_context_data(**kwargs)
        chamado = Chamado.objects.filter(id=self.get_object().id).first()
        if self.template_name == "core/detail.html" and chamado.usuario == self.request.user:
            chamado.novidade = False
            chamado.save()
        fila = FilaChamados.objects.filter(chamado=chamado).first()
        respostas = ChamadoResposta.objects.filter(chamado=self.get_object().id).order_by("data")
        imagens = ChamadoAnexo.objects.filter(chamado=self.get_object().id)
        assinaturas = ChamadoAssinatura.objects.filter(chamado=self.get_object().id)
        reaberturas = ChamadoReaberto.objects.filter(chamado=self.get_object().id)
        if chamado.setor_solicitante is not None:
            setor = s_helper.get_setor(chamado.setor_solicitante)
            setor_solicitante = setor.set_nome
        else:
            setor_solicitante = ''

        try:
            if SetorChamado.objects.get(setor_id=self.request.session['setor_id']).id == chamado.setor.id:
                context['atende'] = True
            else:
                context['atende'] = False
        except:
            context['atende'] = False
        context['respostas'] = respostas
        context['imagens'] = imagens
        context['num_respostas'] = respostas.count()
        context['num_imagens'] = imagens.count()
        context['num_assinaturas'] = assinaturas.count()
        context['num_reaberturas'] = reaberturas.count()
        context['setor_solicitante'] = setor_solicitante
        context['localizacao'] = chamado.localizacao
        context['pavimento'] = chamado.pavimento

        if fila != None:
            context['atendente'] = fila.usuario
        return context

#--------------------------------------------------------------------------------------
# Retorna JSON lista de respostas chamado
#--------------------------------------------------------------------------------------
def respostas_json(request, id_chamado):
    resposta = []

    if id_chamado == None or id_chamado == '' or id_chamado == '0':
        respostas = ChamadoResposta.objects.filter(chamado_id=None)
    else:
        respostas = ChamadoResposta.objects.filter(chamado_id=id_chamado)

    for r in respostas:
        resposta_json = {}
        resposta_json['resposta_id'] = r.id
        resposta_json['chamado_id'] = r.chamado.id
        resposta_json['data'] = r.data.strftime("%d/%m/%Y %H:%M")
        resposta_json['usuario'] = r.usuario.username
        # resposta_json['resposta'] = str.replace(r.resposta, '\n', '<br/>')
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
            fila = FilaManager()
            fila.responde(request.user, chamado)
            #envia_email(chamado)
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
            fila = FilaManager()
            fila.fecha(request.user, chamado)
            #chamado.status = 'FECHADO'
            #chamado.save()
            #envia_email(chamado)

            #historico = HistoricoChamados.objects.create(chamado=chamado, status='FECHADO')
            #historico.save()
        else:
            raise ValueError('Chamado inválido.')
    return HttpResponseRedirect('/fila/')

#--------------------------------------------------------------------------------------
# De acordo com o setor da pessoa logada, direciona para a página inicial
#--------------------------------------------------------------------------------------
class MyIndexView(SuccessMessageMixin, TemplateView):
    template_name = 'core/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user .is_anonymous or not request.user.is_authenticated or 'setor_id' not in request.session:
            return HttpResponseRedirect('/autentica/loga/?next=/')
        try:
            setor_chamado = SetorChamado.objects.get(setor_id=request.session['setor_id'])
            if (setor_chamado.recebe_chamados):
                return HttpResponseRedirect('/fila/')
            else:
                return HttpResponseRedirect('/chamado/')
        except:
            return HttpResponseRedirect('/chamado/')

#--------------------------------------------------------------------------------------
# Quando um atendente reabre um chamado
#--------------------------------------------------------------------------------------
def reabre_json(request):
    chamado_id = request.GET.get('chamado_id', None)
    motivo = request.GET.get('motivo', None)

    if chamado_id != None and chamado_id != '':
        chamado = Chamado.objects.get(pk=chamado_id)
        fila = FilaManager()
        fila.reabre(request.user, chamado, motivo)
        response = JsonResponse({'status':'true','message':'Chamado reaberto com sucesso'}, status=200)
    else:
        response = JsonResponse({'status':'false','message':'Nenhum chamado selecionado'}, status=401)
    return response

# --------------------------------------------------------------------------------------
# Retorna JSON com informação de patrimônio do grupo de serviço
# --------------------------------------------------------------------------------------
def patrimonio_servico_json(request, id_gs):
    resposta = []

    if id_gs == None or id_gs == '' or id_gs == '99999':
        gs_json = {}
    else:
        gs_json = {}
        grupo = GrupoServico.objects.get(pk=id_gs)
        gs_json['patrimonio_obrigatorio'] = grupo.patrimonio_obrigatorio

    resposta.append(gs_json)

    return JsonResponse(resposta, safe=False)    
# --------------------------------------------------------------------------------------
# Retorna JSON das localizacoes cadastradas
# --------------------------------------------------------------------------------------
def localizacao_json(request):
    resposta = [{"localizacao_id": 0, "localizacao_descricao": "----------"}]

    localizacoes = Localizacao.objects.all().order_by('descricao')

    for l in localizacoes:
        localizacao_json = {}
        localizacao_json['localizacao_id'] = l.id
        localizacao_json['localizacao_descricao'] = l.descricao
        resposta.append(localizacao_json)


    return JsonResponse(resposta, safe=False)    
#--------------------------------------------------------------------------------------
# Retorna JSON dos pavimentos da localizacao
#--------------------------------------------------------------------------------------
def pavimentos_json(request, id_localizacao):
    resposta = [{"localizacao_id": 0, "pavimento_descricao": "----------", "pavimento_id": 0}]

    if id_localizacao == None or id_localizacao == '' or id_localizacao == '0':
        respostas = Pavimento.objects.filter(localizacao_id=None).order_by('descricao')
    else:
        respostas = Pavimento.objects.filter(localizacao_id=id_localizacao).order_by('descricao')

    for r in respostas:
        resposta_json = {}
        resposta_json['pavimento_id'] = r.id
        resposta_json['localizacao_id'] = r.localizacao.id
        resposta_json['pavimento_descricao'] = r.descricao
        
        resposta.append(resposta_json)

    return JsonResponse(resposta, safe=False)            
# --------------------------------------------------------------------------------------
# Retorna JSON com informação de localizacao do setor
# --------------------------------------------------------------------------------------
def localizacao_setor_json(request, id_setor):
    resposta = []

    if id_setor == None or id_setor == '' or id_setor == '99999':
        l_json = {}
    else:
        l_json = {}
        setor = SetorChamado.objects.filter(id=id_setor)
        if setor.exists():
            setor = setor.first()
            l_json['localizacao'] = setor.localizacao
        else:
            l_json['localizacao'] = False

    resposta.append(l_json)

    return JsonResponse(resposta, safe=False)        

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class ServicoIndexView(ChamadosAdminRequired, SuccessMessageMixin, FormView):
    template_name = 'core/cadastro/servico/index.html'
    form_class = ServicoSearchForm

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class ServicoCreateView(ChamadosAdminRequired, SuccessMessageMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    success_url = '/cadastro/servico/'
    success_message = "Serviço criado com sucesso"
    template_name = 'core/cadastro/servico/create.html'   
#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class ServicoUpdateView(ChamadosAdminRequired, SuccessMessageMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    success_url = '/cadastro/servico/'
    success_message = "Serviço alterado com sucesso"
    template_name = 'core/cadastro/servico/update.html'

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
def exclui_servico_json(request, pk):

    if request.method == 'POST' and request.is_ajax():
        if pk != None and pk != '':
            servico = Servico.objects.get(pk=pk)
            servico.delete()
            response = JsonResponse({'status':'true','message':'Serviço excluído com sucesso'}, status=200)
        else:
            response = JsonResponse({'status':'false','message':'Erro ao excluir serviço'}, status=401)
    else:
        response = JsonResponse({'status':'false','message':'Não foi possível localizar o serviço'}, status=401)
    return response             

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class GrupoServicoIndexView(ChamadosAdminRequired, SuccessMessageMixin, TemplateView):
    template_name = 'core/cadastro/grupo_servico/index.html'

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class GrupoServicoCreateView(ChamadosAdminRequired, SuccessMessageMixin, CreateView):
    model = GrupoServico
    form_class = GrupoServicoForm
    success_url = '/cadastro/grupo_servico/'
    success_message = "Grupo Serviço criado com sucesso"
    template_name = 'core/cadastro/grupo_servico/create.html'   

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.setor = SetorChamado.objects.get(setor_id=self.request.session['setor_id'])
        obj.save()
        #messages.success(self.success_message)
        return super().form_valid(form)

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class GrupoServicoUpdateView(ChamadosAdminRequired, SuccessMessageMixin, UpdateView):
    model = GrupoServico
    form_class = GrupoServicoForm
    success_url = '/cadastro/grupo_servico/'
    success_message = "Grupo Serviço alterado com sucesso"
    template_name = 'core/cadastro/grupo_servico/update.html'

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
def exclui_grupo_servico_json(request, pk):

    if request.method == 'POST' and request.is_ajax():
        if pk != None and pk != '':
            grupo = GrupoServico.objects.get(pk=pk)
            grupo.delete()
            response = JsonResponse({'status':'true','message':'Grupo Serviço excluído com sucesso'}, status=200)
        else:
            response = JsonResponse({'status':'false','message':'Erro ao excluir grupo serviço'}, status=401)
    else:
        response = JsonResponse({'status':'false','message':'Não foi possível localizar o grupo serviço'}, status=401)
    return response                 

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
def relatorio(request):
    if request.method == 'POST':
        form = RelatorioSetorForm(request, request.POST)

        if form.is_valid():

            chamados = Chamado.objects.filter(setor__setor_id=request.session['setor_id'])

            if form['setor'].value() != '':
                s_helper = ServiceHelper()
                setor = s_helper.get_setor(form['setor'].value())
                setor_solicitante = setor.set_nome
                chamados = chamados.filter(setor_solicitante=setor.set_id)
            else:
                setor_solicitante = 'TODOS OS SETORES'

            data_inicio = datetime.strptime(form['data_inicio'].value(), '%d/%m/%Y')
            chamados = chamados.filter(data_abertura__gte=data_inicio)

            if form['data_fim'].value() != '':
                data_fim = datetime.strptime(form['data_fim'].value(), '%d/%m/%Y')
                data_fim = data_fim + timedelta(days=1)
                #chamados = chamados.filter(Q(data_fechamento=None) or Q(data_fechamento__lte=data_fim))
                #chamados = chamados.filter(Q(data_fechamento__isnull=True) or Q(data_fechamento__lte=data_fim))
                chamados = chamados.exclude(data_fechamento__gt=data_fim)

            if form['grupo_servico'].value() != '':
                chamados = chamados.filter(grupo_servico=form['grupo_servico'].value())            

            chamados = chamados.order_by('data_abertura')
            
            context = {'chamados': chamados, 'inicio': form['data_inicio'].value(), 'fim': form['data_fim'].value(), 'setor': request.session['setor_nome'], 'setor_solicitante': setor_solicitante}
            filename = fill_template('relatorio2.odt', context, output_format='pdf')
            visible_filename = 'relatorio_chamados.pdf'
            return FileResponse(filename, visible_filename)
        else:
            return render(request, 'core/relatorio/chamado/index.html', {'form': form})

    else:
        return render(request, 'core/relatorio/chamado/index.html', {'form': form})

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class RelatorioChamadoIndexView(CMCLoginRequired, SuccessMessageMixin, FormView):
    template_name = 'core/relatorio/chamado/index.html'    
    form_class = RelatorioSetorForm

    def get_form_kwargs(self):
        kwargs = super(RelatorioChamadoIndexView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
        

# --------------------------------------------------------------------------------------
# Retorna JSON dos setores
# --------------------------------------------------------------------------------------
def setores_json(request):
    resposta = []

    setores = SetorChamado.objects.all()

    for s in setores:
        setor_json = {}
        setor_json['id'] = s.id
        setor_json['setor_id'] = s.setor_id
        setor_json['set_nome'] = s.get_nome()
        setor_json['set_sigla'] = s.get_sigla()
        setor_json['recebe_chamados'] = s.recebe_chamados
        resposta.append(setor_json)

    return JsonResponse(resposta, safe=False)

# --------------------------------------------------------------------------------------
# Index para cadastro de setores
# --------------------------------------------------------------------------------------
class SetorChamadoIndexView(ChamadosAdminRequired, SuccessMessageMixin, TemplateView):
    template_name = 'core/cadastro/setor/index.html'    

#--------------------------------------------------------------------------------------
# Create para cadastro de setores
# --------------------------------------------------------------------------------------
class SetorChamadoCreateView(ChamadosAdminRequired, SuccessMessageMixin, CreateView):
    template_name = "core/cadastro/setor/new.html"
    form_class = SetorChamadoForm
    model = SetorChamado
    success_url = '/cadastro/setor/'
    success_message = "Setor criado com sucesso"

#--------------------------------------------------------------------------------------
# Update para cadastro de setores
# --------------------------------------------------------------------------------------
class SetorChamadoUpdateView(ChamadosAdminRequired, SuccessMessageMixin, UpdateView):
    model = SetorChamado
    form_class = SetorChamadoForm
    success_url = '/cadastro/setor/'
    success_message = "Setor alterado com sucesso"
    template_name = 'core/cadastro/setor/update.html'    

#--------------------------------------------------------------------------------------
# Delete para cadastro de setores
# --------------------------------------------------------------------------------------
def exclui_setor_json(request, pk):

    if request.method == 'POST' and request.is_ajax():
        if pk != None and pk != '':
            setor = SetorChamado.objects.get(pk=pk)
            try:
                setor.delete()
            except:
                response = JsonResponse({'status':'false','message':'Não foi possível excluir o setor'}, status=401)    
            response = JsonResponse({'status':'true','message':'Setor excluído com sucesso'}, status=200)
        else:
            response = JsonResponse({'status':'false','message':'Erro ao excluir setor'}, status=401)
    else:
        response = JsonResponse({'status':'false','message':'Não foi possível localizar o setor'}, status=401)
    return response                 

# --------------------------------------------------------------------------------------
# Index para mensagem de acesso restrito admin
# --------------------------------------------------------------------------------------
class AcessoAdmin(TemplateView):
    template_name = 'pages/admin_restricted.html'        

# --------------------------------------------------------------------------------------
# Index para mensagem de acesso restrito atendimento
# --------------------------------------------------------------------------------------
class AcessoAtendente(TemplateView):
    template_name = 'pages/atende_restricted.html'            

#--------------------------------------------------------------------------------------
# Relatorio Chamados
#--------------------------------------------------------------------------------------        
class RelatorioChamados(CMCReportView):
    template_name = 'core/relatorio/chamado/chamados.html'
    download_filename = 'relatorio_chamados.pdf'
    pac_id = None
    chamados = []

    def get_context_data(self, **kwargs):
        context = super(CMCReportView, self).get_context_data(**kwargs)
        context['title'] = 'Relatório de Chamados'
        context['pagesize'] = 'A4 landscape'
        context['chamados'] = self.chamados
        context['inicio'] = self.inicio
        context['fim'] = self.fim
        context['setor'] = self.setor
        context['setor_solicitante'] = self.setor_solicitante
        return context

    def post(self, request, *args, **kwargs):
        context = super(CMCReportView, self).get_context_data(**kwargs)
        form = RelatorioSetorForm(request, request.POST)
        if form.is_valid():

            chamados = Chamado.objects.filter(setor__setor_id=request.session['setor_id'])

            if form['setor'].value() != '':
                s_helper = ServiceHelper()
                setor = s_helper.get_setor(form['setor'].value())
                setor_solicitante = setor.set_nome
                chamados = chamados.filter(setor_solicitante=setor.set_id)
            else:
                setor_solicitante = 'TODOS OS SETORES'

            data_inicio = datetime.strptime(form['data_inicio'].value(), '%d/%m/%Y')
            chamados = chamados.filter(data_abertura__gte=data_inicio)

            if form['data_fim'].value() != '':
                data_fim = datetime.strptime(form['data_fim'].value(), '%d/%m/%Y')
                data_fim = data_fim + timedelta(days=1)
                chamados = chamados.exclude(data_fechamento__gt=data_fim)

            if form['grupo_servico'].value() != '':
                chamados = chamados.filter(grupo_servico=form['grupo_servico'].value())            

            chamados = chamados.order_by('data_abertura')
            self.chamados = chamados
            self.inicio = form['data_inicio'].value()
            self.fim = form['data_fim'].value()
            self.setor = request.session['setor_nome']
            self.setor_solicitante = setor_solicitante
            return super(RelatorioChamados, self).get(request, *args, **kwargs)      
        else:
            return render(request, 'core/relatorio/chamado/index.html', {'form': form})

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------
class ConsolidadoChamadoEditlView(ChamadosAtendenteRequired, SuccessMessageMixin, DetailView):
    template_name = "core/edit.html"
    model = Chamado
    success_url = '/fila/'
    success_message = "Chamado atualizadao com sucesso"

    def get_context_data(self, **kwargs):
        s_helper = ServiceHelper()

        context = super(DetailView, self).get_context_data(**kwargs)
        chamado = Chamado.objects.filter(id=self.get_object().id).first()
        fila = FilaChamados.objects.filter(chamado=chamado).first()
        respostas = ChamadoResposta.objects.filter(chamado=self.get_object().id).order_by("data")
        imagens = ChamadoAnexo.objects.filter(chamado=self.get_object().id)
        assinaturas = ChamadoAssinatura.objects.filter(chamado=self.get_object().id).order_by("email")
        reaberturas = ChamadoReaberto.objects.filter(chamado=self.get_object().id)
        if chamado.setor_solicitante is not None:
            setor = s_helper.get_setor(chamado.setor_solicitante)
            setor_solicitante = setor.set_nome
        else:
            setor_solicitante = ''

        context['respostas'] = respostas
        context['imagens'] = imagens
        context['assinaturas'] = assinaturas
        context['num_respostas'] = respostas.count()
        context['num_imagens'] = imagens.count()
        context['num_assinaturas'] = assinaturas.count()
        context['num_reaberturas'] = reaberturas.count()
        context['setor_solicitante'] = setor_solicitante
        context['MSCMC_SERVER'] = settings.MSCMC_SERVER
        if fila != None:
            context['atendente'] = fila.usuario
        return context

#--------------------------------------------------------------------------------------
# Retorna JSON lista de assinaturas chamado
#--------------------------------------------------------------------------------------
def assinaturas_json(request, id_chamado):
    assinatura = []

    if id_chamado == None or id_chamado == '' or id_chamado == '0':
        assinaturas = ChamadoAssinatura.objects.filter(chamado_id=None)
    else:
        assinaturas = ChamadoAssinatura.objects.filter(chamado_id=id_chamado)

    for a in assinaturas:
        assinatura_json = {}
        assinatura_json['assinatura_id'] = a.id
        assinatura_json['chamado_id'] = a.chamado.id
        assinatura_json['email'] = a.email
        
        assinatura.append(assinatura_json)

    return JsonResponse(assinatura, safe=False)        

# -----------------------------------------------------------------------------------
# chamada API para consumir usuarios LDAP
# -----------------------------------------------------------------------------------
def consome_usuarios_ldap(request):
    consumer = MSCMCConsumer()
    return consumer.consome_usuarios_ldap()

#--------------------------------------------------------------------------------------
# Salva uma assinatura
#--------------------------------------------------------------------------------------
def assina_json(request):

    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('id_chamado') != None and request.POST.get('id_chamado') != '':
            chamado = Chamado.objects.get(pk=request.POST.get('id_chamado'))
            ChamadoAssinatura.objects.create(chamado=chamado, email=request.POST.get('selectassinatura'))
            response = JsonResponse({'status':'true','message':'Assinatura criada com sucesso'}, status=200)
        else:
            response = JsonResponse({'status':'false','message':'Chamado inválido'}, status=401)
    else:
        response = JsonResponse({'status':'false','message':'Nenhum chamado selecionado'}, status=401)
    return response        

#--------------------------------------------------------------------------------------
# Exclui uma assinatura
#--------------------------------------------------------------------------------------
def exclui_assina_json(request):

    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('assinatura_id') != None and request.POST.get('assinatura_id') != '':
            assinatura = ChamadoAssinatura.objects.get(pk=request.POST.get('assinatura_id'))
            assinatura.delete()
            response = JsonResponse({'status':'true','message':'Assinatura excluída com sucesso'}, status=200)
        else:
            response = JsonResponse({'status':'false','message':'Assinatura inválida'}, status=401)
    else:
        response = JsonResponse({'status':'false','message':'Nenhuma assinatura selecionada'}, status=401)
    return response            

#--------------------------------------------------------------------------------------
# Imprime chamado
#--------------------------------------------------------------------------------------        
class ImprimeChamado(CMCReportView):
    template_name = 'core/relatorio/chamado/chamado.html'
    download_filename = 'chamado.pdf'

    def get_context_data(self, **kwargs):
        context = super(CMCReportView, self).get_context_data(encoding =u"utf-8", **kwargs)
        context['title'] = 'Dados do Chamado'
        context['pagesize'] = 'A4 portrait'
        context['chamado'] = self.chamado
        context['completo'] = self.completo
        context['setor_solicitante'] = self.setor_solicitante
        context['atendente'] = self.atendente
        context['respostas'] = self.respostas
        context['assinaturas'] = self.assinaturas
        context['historicos'] = self.historicos
        context['reaberturas'] = self.reaberturas
        context['localizacao'] = self.localizacao
        context['pavimento'] = self.pavimento

        return context

    def get(self, request, *args, **kwargs):
        s_helper = ServiceHelper()

        context = super(CMCReportView, self).get_context_data(encoding =u"utf-8", **kwargs)
        #id_chamado = kwargs.get('id_chamado', None)
        #opt = kwargs.get('opt', False)

        id_chamado = request.GET.get('id_chamado', None)
        opt = request.GET.get('opt', None)

        if id_chamado is not None:
            chamado = Chamado.objects.get(pk=id_chamado)
            if chamado.setor_solicitante is not None:
                setor = s_helper.get_setor(chamado.setor_solicitante)
                setor_solicitante = setor.set_nome
            else:
                setor_solicitante = ''

            fila = FilaChamados.objects.filter(chamado=chamado).first()
            if fila != None:
                self.atendente = fila.usuario
            else:
                self.atendente = None

            respostas = ChamadoResposta.objects.filter(chamado=chamado).order_by("data")

            assinaturas = ChamadoAssinatura.objects.filter(chamado=chamado).order_by("email")

            historicos = HistoricoChamados.objects.filter(chamado=chamado).order_by("data")

            reaberturas = ChamadoReaberto.objects.filter(chamado=chamado).order_by("reaberto")

            if opt is None or opt == '1':
                self.completo = False
            else:
                self.completo = True

            self.chamado = chamado
            self.setor_solicitante = setor_solicitante
            self.respostas = respostas
            self.assinaturas = assinaturas
            self.historicos = historicos
            self.reaberturas = reaberturas
            self.localizacao = chamado.localizacao
            self.pavimento = chamado.pavimento

        return super(ImprimeChamado, self).get(request, *args, **kwargs)      

#--------------------------------------------------------------------------------------
# Retorna JSON lista de reaberturas chamado
#--------------------------------------------------------------------------------------
def reaberturas_json(request, id_chamado):
    reabertura = []

    if id_chamado == None or id_chamado == '' or id_chamado == '0':
        reaberturas = ChamadoReaberto.objects.filter(chamado_id=None)
    else:
        reaberturas = ChamadoReaberto.objects.filter(chamado_id=id_chamado)

    for r in reaberturas:
        reabertura_json = {}
        reabertura_json['reabertura_id'] = r.id
        reabertura_json['chamado_id'] = r.chamado.id
        reabertura_json['data_reabertura'] = r.reaberto.strftime("%d/%m/%Y %H:%M")
        reabertura_json['motivo'] = r.motivo
        
        reabertura.append(reabertura_json)

    return JsonResponse(reabertura, safe=False)                