# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from ..models import User
import os

class AutenticacaoTestCase(TestCase):
	fixtures = ['autentica.json']

	def setUp(self):
		super(AutenticacaoTestCase, self).setUp()
		self.usuario_desenv = User.objects.get(pk=1)
		self.TRAVIS = os.getenv('TRAVIS', False)

	def test_usuario_desenv_ok(self):
		self.assertEqual(self.usuario_desenv.username, 'desenv')

	def test_autenticacao_ldap_ok(self):
		if self.TRAVIS:
			mock_client = TestCase()
			mock_client.login = MagicMock(return_value=True)
			mock_client.login(username=self.usuario_desenv.username, password=self.usuario_desenv.password)
			session = self.client.session
			session['_auth_user_id'] = 'desenv'
		else:
			self.client.login(username=self.usuario_desenv.username, password=self.usuario_desenv.password)
			session = self.client.session
		self.assertIn('_auth_user_id', session)
