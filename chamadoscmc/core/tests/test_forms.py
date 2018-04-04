# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from django.db import IntegrityError, DataError
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest

from ..forms import ChamadoForm, FilaChamadosForm, RelatorioSetorForm, SetorChamadoForm
from autentica.models import User
from ..models import SetorChamado, GrupoServico, Servico
from consumer.lib.msconsumer import Setor

from .factories import SetorChamadoFactory, ServicoFactory, GrupoServicoFactory

import os

class ComboSetorChamado(object):
    def __init__(self, id, get_nome):  
        self.id = id
        self.get_nome = get_nome

    def get_nome(self):
        return self.get_nome


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
    #fixtures = ['user.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

    @patch('chamadoscmc.core.models.SetorChamado.__str__')
    def setUp(self, __str__mock):
        __str__mock.return_value = "PINEU"
        self.user = get_user_model().objects.create_user('administrador')
        self.setor = SetorChamadoFactory()
        self.grupo_servico = GrupoServicoFactory(setor=self.setor, descricao='Grupo de serviço')
        self.servico = ServicoFactory(grupo_servico=self.grupo_servico, descricao='Servico')

    @patch('chamadoscmc.core.forms.ChamadoForm.ret_setores')
    @patch('chamadoscmc.core.models.SetorChamado.__str__')        
    def test_init(self, ret_setores_mock, __str__mock):
        ret_setores = [('1', 'Divisão de Desenvolvimento de Sistemas')]
        ret_setores_mock.return_value = ret_setores
        __str__mock.return_value = "PINEU"
        form = ChamadoForm()

    @patch('chamadoscmc.core.forms.ChamadoForm.ret_setores')
    @patch('chamadoscmc.core.models.SetorChamado.__str__')
    def test_inclui_ok(self, ret_setores_mock, __str__mock):
        ret_setores = [('1', 'Divisão de Desenvolvimento de Sistemas')]
        ret_setores_mock.return_value = ret_setores
        __str__mock.return_value = "PINEU"
        form_data = {'usuario':"1", 'setor':self.setor.id, 'grupo_servico':self.grupo_servico.id, 'servico':self.servico.id, 'ramal':"4813",
                     'assunto':"mouse não funciona", 'descricao':"já tentei de tudo mas não vai"}
        form = ChamadoForm(data=form_data)
        #print(form)
        self.assertTrue(form.is_valid())

    @patch('chamadoscmc.core.forms.ChamadoForm.ret_setores')
    def test_inclui_setor_vazio(self, ret_setores_mock):
        ret_setores = [('1', 'Divisão de Desenvolvimento de Sistemas')]
        ret_setores_mock.return_value = ret_setores

        form_data = {'usuario':"1", 'grupo_servico':self.grupo_servico.id, 'servico':self.servico.id, 'ramal':"4813",
                     'assunto':"mouse não funciona", 'descricao':"já tentei de tudo mas não vai"}
        form = ChamadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        #self.assertEqual(form.cleaned_data['usuario'], usuario)

    @patch('chamadoscmc.core.forms.ChamadoForm.ret_setores')
    def test_inclui_servico_vazio(self, ret_setores_mock):
        ret_setores = [('1', 'Divisão de Desenvolvimento de Sistemas')]
        ret_setores_mock.return_value = ret_setores

        form_data = {'usuario':"1", 'setor':self.setor.id, 'grupo_servico':self.grupo_servico.id, 'ramal':"4813",
                     'assunto':"mouse não funciona", 'descricao':"já tentei de tudo mas não vai"}
        form = ChamadoForm(data=form_data)
        self.assertFalse(form.is_valid())

class ChamadoRelatorioFormTest(TestCase):
    fixtures = ['user.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']        

    def setUp(self):
        user = get_user_model().objects.create_user('administrador')
        self.factory = RequestFactory()

    @patch('chamadoscmc.core.forms.RelatorioSetorForm.get_grupos')
    @patch('consumer.lib.helper.ServiceHelper.get_setores_combo')
    def test_init(self,get_grupos_mock, get_setores_combo_mock):
        ret_grupos = []
        ret_setores = []
        get_grupos_mock.return_value = ret_grupos
        get_setores_combo_mock.return_value = ret_setores
        request = HttpRequest()
        form = RelatorioSetorForm(request)

    @patch('chamadoscmc.core.forms.RelatorioSetorForm.get_grupos')
    @patch('consumer.lib.helper.ServiceHelper.get_setores_combo')
    def test_gera_ok(self, get_grupos_mock, get_setores_combo_mock):
        ret_grupos = []
        ret_setores = []
        get_grupos_mock.return_value = ret_grupos
        get_setores_combo_mock.return_value = ret_setores
        request = HttpRequest()
        form_data = {'setor': "", 'data_inicio': "19/03/2018", 'data_fim': "19/03/2018", 'grupo_servico': ""}
        form = RelatorioSetorForm(request, data=form_data)
        self.assertTrue(form.is_valid())

    @patch('chamadoscmc.core.forms.RelatorioSetorForm.get_grupos')
    @patch('consumer.lib.helper.ServiceHelper.get_setores_combo')
    def test_gera_data_inicio_invalida(self, get_grupos_mock, get_setores_combo_mock):
        ret_grupos = []
        ret_setores = []
        get_grupos_mock.return_value = ret_grupos
        get_setores_combo_mock.return_value = ret_setores
        request = HttpRequest()
        form_data = {'setor': "", 'data_inicio': "", 'data_fim': "19/03/2018", 'grupo_servico': ""}
        form = RelatorioSetorForm(request, data=form_data)
        self.assertFalse(form.is_valid())

class SetorChamadoFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('zaquinha', password='zaca')
        self.user.is_staff = True
        self.user.lotado = 171
        self.user.matricula = 2179
        self.user.save()
        self.factory = RequestFactory()

    @patch('consumer.lib.helper.ServiceHelper.get_setores')
    def test_init(self, get_setores_mock):
        ret_setores = []
        get_setores_mock.return_value = ret_setores
        form = SetorChamadoForm()

    @patch('consumer.lib.helper.ServiceHelper.get_setores')
    def test_grava_ok(self, get_setores_mock):
        ret_setores = [Setor(171, 'Pinéu', 'PI', None, True, None)]
        get_setores_mock.return_value = ret_setores
        form_data = {'setor_id': 171, 'recebe_chamados': True, 'localizacao': False}
        form = SetorChamadoForm(data=form_data)
        self.assertTrue(form.is_valid())

    @patch('consumer.lib.helper.ServiceHelper.get_setores')        
    def test_grava_setor_nulo(self, get_setores_mock):
        ret_setores = []
        get_setores_mock.return_value = ret_setores
        form_data = {'setor': None, 'recebe_chamados': True, 'localizacao': False}
        form = SetorChamadoForm(data=form_data)
        self.assertFalse(form.is_valid())