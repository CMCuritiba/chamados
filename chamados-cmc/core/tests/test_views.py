# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch, MagicMock, Mock
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from ..views import CadastroChamadosIndexView

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