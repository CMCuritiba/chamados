# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock, Mock
from django.db import IntegrityError, DataError
from ..models import SetorChamado, GrupoServico, VSetor
import os

class SetorChamadoTestCase(TestCase):
	fixtures = ['setor_chamado.json']

	def setUp(self):
		super(SetorChamadoTestCase, self).setUp()

	def test_setor_chamado_ok(self):
		setor_chamado = SetorChamado.objects.get(pk=1)
		self.assertEqual(setor_chamado.setor.set_nome, 'Divisão de Desenvolvimento De Sistemas')

	def test_setor_chamado_setor_nulo(self):
		with self.assertRaises(IntegrityError):
			setor_chamado = SetorChamado.objects.create(setor=None, recebe_chamados=True)

	def test_setor_chamado_setor_unico(self):
		with self.assertRaises(IntegrityError):
			vsetor = VSetor.objects.get(pk=171)
			setor_chamado = SetorChamado.objects.create(setor=vsetor, recebe_chamados=True)

class GrupoServicoTestCase(TestCase):
	fixtures = ['setor_chamado.json', 'grupo_servico.json']

	def setUp(self):
		super(GrupoServicoTestCase, self).setUp()			

	def test_grupo_setor_1(self):
		grupo = GrupoServico.objects.get(pk=1)
		setor_chamado = SetorChamado.objects.get(pk=1)
		self.assertEqual(grupo.descricao, 'SPL')
		self.assertEqual(grupo.setor, setor_chamado)

	def test_grupo_setor_vazio(self):
		with self.assertRaises(IntegrityError):
			grupo = GrupoServico.objects.create(descricao='tem que gerar um erro')

	def test_grupo_descricao_maior_300(self):
		setor_chamado = SetorChamado.objects.get(pk=1)
		with self.assertRaises(DataError):
			grupo = GrupoServico.objects.create(setor=setor_chamado, descricao='1'*301)

	def test_grupo_descricao_vazio(self):
		setor_chamado = SetorChamado.objects.get(pk=1)
		with self.assertRaises(IntegrityError):
			grupo = GrupoServico.objects.create(setor=setor_chamado, descricao=None)
