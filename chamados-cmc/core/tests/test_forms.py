# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from django.db import IntegrityError, DataError
from django.contrib.auth import get_user_model

import os

class FilaChamadosFormTest(TestCase):
	fixtures = ['chamados.json']

	def setUp(self):
		self.user = get_user_model().objects.create_user('zaquinha', password='zaca')
		self.user.is_staff = True
		self.user.lotado = 171
		self.user.matricula = 2179
		self.user.save()
		self.factory = RequestFactory()

	def test_init(self):
		form = RamalPesquisaForm()