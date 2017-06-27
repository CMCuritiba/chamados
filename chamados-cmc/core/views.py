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

from ..autentica.util.mixin import CMCLoginRequired
from .forms import ChamadoForm
from .models import Chamado

class CadastroChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, FormView):
	template_name = 'cadastro/index.html'
	form_class = ChamadoForm

#--------------------------------------------------------------------------------------
class CadastroChamadosCreateView(CMCLoginRequired, SuccessMessageMixin, CreateView):
	template_name = "cadastro/new.html"
	form_class = ChamadoForm
	model = Chamado
	success_url = '/cadastro/'
	success_message = "Chamado criado com sucesso"