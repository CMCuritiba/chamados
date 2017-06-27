# -*- coding: utf-8 -*-

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView, CreateView
from ..autentica.util.mixin import CMCLoginRequired
from .forms import ChamadoForm
from .models import Chamado

class CadastroChamadosIndexView(CMCLoginRequired, SuccessMessageMixin, FormView):
	template_name = 'cadastro/index.html'
	form_class = ChamadoForm


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
class CadastroChamadosCreateView(CMCLoginRequired, SuccessMessageMixin, CreateView):
	template_name = "cadastro/new.html"
	form_class = ChamadoForm
	model = Chamado
	success_url = '/cadastro/'
	success_message = "Chamado criado com sucesso"
