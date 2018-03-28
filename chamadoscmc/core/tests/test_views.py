# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch, MagicMock, Mock
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import TestCase, RequestFactory

from ..views import CadastroChamadosIndexView, FilaChamadosIndexView, ChamadoDetailView, GrupoServicoIndexView, RelatorioChamadoIndexView, SetorChamadoIndexView, SetorChamadoCreateView, SetorChamadoUpdateView
from autentica.models import User

from .factories import SetorChamadoFactory


class ChamadoViewTests(TestCase):
    fixtures = ['user.json', 'chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

    nome_usuario = 'tora'
    senha = 'mandioca'


    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.save()
        self.factory = RequestFactory()


    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()


    def test_index_table_sem_chamados(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = CadastroChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chamados')
        self.assertContains(response, 'Você nunca abriu algum chamado')


    def test_index_table_com_chamados(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = CadastroChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chamados')
        self.assertContains(response, 'Chamados realizados pelo usuário')


class FilaChamadosViewTests(TestCase):
    fixtures = ['user.json', 'chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json', 'chamado.json',
                'fila_chamados.json']


    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.is_staff = True
        self.user.save()
        self.factory = RequestFactory()


    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()


    def test_index(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = CadastroChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Abertura de Chamados')


    def test_index_table_chamados(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = CadastroChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Abertura de Chamados')


    def test_url(self):
        request = self.factory.get('/fila/')
        request.user = self.user
        response = FilaChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Alexandre Odoni')


class FilaChamadosViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('zaca', password='zaca')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.factory = RequestFactory()


'''
    def test_url(self):
        request = self.factory.get('/chamados/index/')
        request.user = self.user
        response = FilaChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'Alexandre Odoni')
'''

class GrupoServicoViewTests(TestCase):
    fixtures = ['user.json', 'chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

    nome_usuario = 'tora'
    senha = 'mandioca'


    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.factory = RequestFactory()


    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()


    def test_index(self):
        request = self.factory.get('/cadastro/grupo_servico/')
        self.setup_request(request)
        response = GrupoServicoIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)


class RelatoriosViewTests(TestCase):
    fixtures = ['user.json', 'chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

    nome_usuario = 'tora'
    senha = 'mandioca'


    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.save()
        self.factory = RequestFactory()


    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()


    @patch('chamadoscmc.core.forms.RelatorioSetorForm.get_grupos')
    @patch('consumer.lib.helper.ServiceHelper.get_setores_combo')
    def test_index(self, get_grupos_mock, get_setores_combo_mock):
        ret_grupos = []
        ret_setores = []
        get_grupos_mock.return_value = ret_grupos
        get_setores_combo_mock.return_value = ret_setores
        request = self.factory.get('/relatorio/chamado/')
        request.user = self.user
        response = RelatorioChamadoIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)        

class SetorChamadoIndexViewTests(TestCase):

    nome_usuario = 'tora'
    senha = 'mandioca'

    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.factory = RequestFactory()

    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session.save()

    def test_index(self):
        request = self.factory.get('/cadastro/setorchamado/')
        request.user = self.user
        response = SetorChamadoIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)        


class SetorChamadoCreateViewTests(TestCase):
    nome_usuario = 'tora'
    senha = 'mandioca'

    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.factory = RequestFactory()

    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session.save()

    @patch('consumer.lib.helper.ServiceHelper.get_setores')        
    def test_get(self, get_setores_mock):
        ret_setores = []
        get_setores_mock.return_value = ret_setores
        request = self.factory.get('/cadastro/setor/new')
        request.user = self.user
        response = SetorChamadoCreateView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)        


class SetorChamadoUpdateViewTests(TestCase):
    nome_usuario = 'tora'
    senha = 'mandioca'

    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.factory = RequestFactory()
        setor = SetorChamadoFactory.create()

    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session.save()

    @patch('consumer.lib.helper.ServiceHelper.get_setores')        
    def test_get(self, get_setores_mock):
        ret_setores = []
        get_setores_mock.return_value = ret_setores
        request = self.factory.get('/cadastro/setor/edit')
        self.setup_request(request)
        request.user = self.user
        response = SetorChamadoUpdateView.as_view()(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 200)                
        self.assertEqual(response.template_name[0], 'core/cadastro/setor/update.html')