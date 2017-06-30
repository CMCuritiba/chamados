# -*- coding: utf-8 -*-

from django import forms
from .models import Chamado
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



class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['usuario', 'setor', 'grupo_servico', 'servico', 'ramal', 'assunto', 'descricao']

    def __init__(self, *args, **kwargs):
        super(ChamadoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
			Div(
				Div('setor', css_class='col-md-12',),
				css_class='col-md-12 row',
			),
			Div(
				Div('grupo_servico', css_class='col-md-6',),
				Div('servico', css_class='col-md-6',),
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
				Div('usuario', css_class='col-md-12',),
				css_class='col-md-12 row hidden',
			),
		)