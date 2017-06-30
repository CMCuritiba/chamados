# -*- coding: utf-8 -*-

from django import forms
from .models import Chamado


class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['usuario', 'setor', 'grupo_servico', 'servico', 'ramal', 'assunto', 'descricao']


class FilaChamadosForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(FilaChamadosForm, self).__init__(*args, **kwargs)