# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from django.db import IntegrityError, DataError
from django.contrib.auth import get_user_model

from ..forms import ChamadoForm, FilaChamadosForm
from autentica.models import User
from ..models import SetorChamado, GrupoServico, Servico

import os

class FilaChamadosFormTest(TestCase):
    fixtures = ['user.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json', 'chamado.json']

    def setUp(self):
        self.user = get_user_model().objects.create_user('zaquinha', password='zaca')
        self.user.is_staff = True
        self.user.lotado = 171
        self.user.matricula = 2179
        self.user.save()
        self.factory = RequestFactory()

    def test_init(self):
        form = FilaChamadosForm()


class ChamadoFormTest(TestCase):
    fixtures = ['user.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

    def setUp(self):
        user = get_user_model().objects.create_user('administrador')


    def test_init(self):
        form = ChamadoForm()


    def test_inclui_ok(self):
        form_data = {'usuario':"1", 'setor':"1", 'grupo_servico':"1", 'servico':"1", 'ramal':"4813",
                     'assunto':"mouse não funciona", 'descricao':"já tentei de tudo mas não vai"}
        form = ChamadoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_inclui_setor_vazio(self):
        usuario = User.objects.get(pk=1)

        form_data = {'usuario':"1", 'grupo_servico':"1", 'servico':"1", 'ramal':"4813",
                     'assunto':"mouse não funciona", 'descricao':"já tentei de tudo mas não vai"}
        form = ChamadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        #self.assertEqual(form.cleaned_data['usuario'], usuario)

    def test_inclui_servico_vazio(self):
        grupo = GrupoServico.objects.get(pk=1)

        form_data = {'usuario':"1", 'setor':"1", 'grupo_servico':"1", 'ramal':"4813",
                     'assunto':"mouse não funciona", 'descricao':"já tentei de tudo mas não vai"}
        form = ChamadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.cleaned_data['grupo_servico'], grupo)