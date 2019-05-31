# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, CharField, DecimalField, DateField, BooleanField
from django.forms.models import inlineformset_factory
from django.forms import formsets, models
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Button, HTML, ButtonHolder
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions, AppendedText)
from crispy_forms.bootstrap import StrictButton
from django.conf import settings
from decimal import Decimal

from django.contrib.sessions.backends.db import SessionStore

from consumer.lib.helper import ServiceHelper

from .models import Chamado, ChamadoResposta, Localizacao, Pavimento, Servico, GrupoServico, SetorChamado


class ChamadoForm(forms.ModelForm):
    
    class Meta:
        model = Chamado
        #fields = ['setor', 'grupo_servico', 'servico', 'ramal', 'assunto', 'descricao', 'patrimonio', 'localizacao', 'pavimento', 'anexo']
        fields = ['setor', 'grupo_servico', 'servico', 'ramal', 'assunto', 'descricao', 'patrimonio', 'localizacao', 'pavimento'] 
        exclude = ('user',)

    def ret_setores(self):
        ob_setores = SetorChamado.objects.filter(recebe_chamados=True)
        ob_setores = sorted(ob_setores, key=lambda a: a.get_nome())
        return [(e.id, e.get_nome()) for e in ob_setores]

    def __init__(self, *args, **kwargs):
        super(ChamadoForm, self).__init__(*args, **kwargs)
        #self.fields['setor'] = forms.ChoiceField(label='Setor',  required=True, widget=forms.Select(attrs={'data-live-search': 'true'}))
        self.fields['localizacao'].empty_label = "Selecione..."
        self.fields['pavimento'].empty_label = "Selecione..."
        self.fields['foto'] = forms.FileField(required=False, label='Foto(s)', widget=forms.FileInput(attrs={'multiple': 'true'}))

        self.fields['grupo_servico'].label = 'Grupo de Serviço'
        self.fields['servico'].label = 'Serviço'
        self.fields['patrimonio'].label = 'Patrimônio'
        self.fields['descricao'].label = 'Descrição'
        self.fields['localizacao'].label = 'Localização'

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.fields['setor'].choices = self.ret_setores()
        self.fields['setor'].choices.insert(0,( '', '-----------'))


        self.helper.layout = Layout(
            Div(
                Div(Field('setor'), css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('grupo_servico', css_class='col-md-4',),
                Div('servico', css_class='col-md-4',),
                Div('patrimonio', css_class='col-md-4',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('ramal', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('assunto', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('descricao', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('localizacao', css_class='col-md-6',),
                Div('pavimento', css_class='col-md-6',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('foto', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )

    def clean(self):
        data = self.cleaned_data
        if 'grupo_servico' in data:
            if data['grupo_servico'] is None:
                raise ValidationError('Grupo Serviço Obrigatório')
            if data['grupo_servico'].patrimonio_obrigatorio:
                if data['patrimonio'] == '' or data['patrimonio'] is None:
                    raise ValidationError('Patrimônio obrigatório para grupo de serviço : ' + data['grupo_servico'].descricao)
        return data

class FilaChamadosForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(FilaChamadosForm, self).__init__(*args, **kwargs)

class ChamadoRespostaForm(forms.ModelForm):
    class Meta:
        model = ChamadoResposta
        fields = ['chamado', 'data', 'usuario', 'resposta']

    def __init__(self, *args, **kwargs):
        super(ChamadoRespostaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
			Div(
				Div('chamado', css_class='col-md-12',),
				css_class='col-md-12 row hidden',
			),
			Div(
				Div('usuario', css_class='col-md-12',),
				css_class='col-md-12 row hidden',
			),
			Div(
				Div('resposta', css_class='col-md-12',),
				css_class='col-md-12 row',
			),
		)

class ServicoSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ServicoSearchForm, self).__init__(*args, **kwargs)

        self.fields['grupo_servico'] = forms.ChoiceField(label="Grupo de Serviço", widget=forms.Select(attrs={'data-live-search': 'true'}))


        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div('grupo_servico', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )

class ServicoForm(forms.ModelForm):

    class Meta:
        model = Servico
        fields = ['grupo_servico', 'descricao']

    def __init__(self, *args, **kwargs):
        super(ServicoForm, self).__init__(*args, **kwargs)

        self.fields['grupo_servico'].label = 'Grupo de Serviço'
        self.fields['descricao'].label = 'Descrição'

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div('grupo_servico', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('descricao', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )        

class GrupoServicoForm(forms.ModelForm):

    class Meta:
        model = GrupoServico
        fields = ['descricao', 'setor', 'patrimonio_obrigatorio']
        exclude = ('setor',)

    def __init__(self, *args, **kwargs):
        super(GrupoServicoForm, self).__init__(*args, **kwargs)

        self.fields['descricao'].label = 'Descrição'
        self.fields['patrimonio_obrigatorio'].label = 'Patrimônio Obrigatório'

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div('descricao', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('patrimonio_obrigatorio', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )                


class RelatorioSetorForm(forms.Form):

    def get_grupos(self, request):
        return GrupoServico.objects.filter(setor__setor_id=request.session['setor_id']).order_by('descricao')


    def __init__(self, request, *args, **kwargs):
        super(RelatorioSetorForm, self).__init__(*args, **kwargs)

        self.fields['data_inicio'] = forms.DateField(label="Data Início")
        self.fields['data_fim'] = forms.DateField(label="Data Fim", required=False)
        self.fields['grupo_servico'] = forms.ChoiceField(label="Grupo de Serviço", required=False, widget=forms.Select(attrs={'data-live-search': 'true'}))
        self.fields['setor'] = forms.ChoiceField(label='Setor Solicitante',  required=False)

        self.service_helper = ServiceHelper()

        ob_setores = self.service_helper.get_setores_combo('TODOS OS SETORES')
        ob_grupos = self.get_grupos(request)

        self.fields['setor'].choices = [(e.set_id, e.set_nome) for e in ob_setores]
        self.fields['grupo_servico'].choices = [(e.id, e.descricao) for e in ob_grupos]

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Div(
                Div(AppendedText('data_inicio', '<span class="glyphicon glyphicon-calendar"></span>'), css_class='col-md-6',),
                Div(AppendedText('data_fim', '<span class="glyphicon glyphicon-calendar"></span>'), css_class='col-md-6',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('grupo_servico', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('setor', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )        

class SetorChamadoForm(forms.ModelForm):

    class Meta:
        model = SetorChamado
        fields = ['setor_id', 'recebe_chamados', 'localizacao']

    def get_setores(self):
        return self.service_helper.get_setores()


    def __init__(self, *args, **kwargs):
        super(SetorChamadoForm, self).__init__(*args, **kwargs)

        self.fields['setor_id'] = forms.ChoiceField(label='Setor',  required=True, widget=forms.Select(attrs={'data-live-search': 'true'}))
        self.fields['recebe_chamados'] = forms.BooleanField(label='Recebe Chamados',  required=False)
        self.fields['localizacao'] = forms.BooleanField(label='Informa Localização',  required=False)

        self.service_helper = ServiceHelper()

        ob_setores = self.get_setores()

        self.fields['setor_id'].choices = [(e.set_id, e.set_nome) for e in ob_setores]

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Div(
                Div('setor_id', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('recebe_chamados', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
            Div(
                Div('localizacao', css_class='col-md-12',),
                css_class='col-md-12 row',
            ),
        )                