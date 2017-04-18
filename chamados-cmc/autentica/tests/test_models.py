# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from ..models import User

class AutenticacaoTestCase(TestCase):
	fixtures = ['autentica.json']

	def setUp(self):
		super(AutenticacaoTestCase, self).setUp()
		self.usuario_desenv = User.objects.get(pk=1)
		self.factory = RequestFactory()

	def test_usuario_desenv_ok(self):
		self.assertEqual(self.usuario_desenv.username, 'desenv')

	def test_autenticacao_ldap_ok(self):
		self.client.login(username=self.usuario_desenv.username, password=self.usuario_desenv.password)
		self.assertIn('_auth_user_id', self.client.session)
