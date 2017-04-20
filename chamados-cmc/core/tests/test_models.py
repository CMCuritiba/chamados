# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from django.db import IntegrityError, DataError
from ..models import Setor
import os

class SetorTestCase(TestCase):
	fixtures = ['setor.json']

	def setUp(self):
		super(SetorTestCase, self).setUp()

	def test_setor_desenvolvimento(self):
		setor = Setor.objects.get(pk=1)
		self.assertEqual(setor.descricao, 'Desenvolvimento')

	def test_setor_descricao_branco(self):
		with self.assertRaises(IntegrityError):
			setor = Setor.objects.create(descricao=None, id_elotech=1001)

	def test_setor_id_elotech_branco(self):
		with self.assertRaises(IntegrityError):
			setor = Setor.objects.create(descricao='Desenvolvimento', id_elotech=None)

	def test_setor_id_elotech_unico(self):
		with self.assertRaises(IntegrityError):
			setor = Setor.objects.create(descricao='Desenvolvimento', id_elotech=1001)