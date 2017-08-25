# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from autentica.models import User
from django.db import IntegrityError, DataError
from ..models import SetorChamado, GrupoServico, VSetor, Servico, Chamado, FilaChamados, ChamadoResposta


class ChamadoTestCase(TestCase):
	fixtures = ['user.json','chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

	def setUp(self):
		super(ChamadoTestCase, self).setUp()

	def test_dummy(self):
		self.assertEqual(1,1)

	def test_chamado_insere_ok(self):
		usuario = User.objects.get(pk=1)
		setor_chamado = SetorChamado.objects.get(pk=1)
		grupo = GrupoServico.objects.get(pk=1)
		servico = Servico.objects.get(pk=1)

		chamado = Chamado.objects.create(usuario=usuario, setor=setor_chamado, grupo_servico=grupo, servico=servico,
										 ramal="4813", assunto="pau no relatório",descricao="copiei texto do editor do "
													"SPL e colei em nova proposição mas quando vou imprimir aparecem "
																			"caracteres estranhos e não imprime PDF.")


	def test_chamado_insere_usuario_nulo(self):
		setor_chamado = SetorChamado.objects.get(pk=1)
		grupo = GrupoServico.objects.get(pk=1)
		servico = Servico.objects.get(pk=1)

		with self.assertRaises(IntegrityError):
			chamado = Chamado.objects.create(usuario=None, setor=setor_chamado, grupo_servico=grupo, servico=servico,
										 ramal="4813", assunto="pau no relatório",descricao="copiei texto do editor do "
													"SPL e colei em nova proposição mas quando vou imprimir aparecem "
																			"caracteres estranhos e não imprime PDF.")


	def test_chamado_insere_setor_nulo(self):
		usuario = User.objects.get(pk=1)
		grupo = GrupoServico.objects.get(pk=1)
		servico = Servico.objects.get(pk=1)

		with self.assertRaises(IntegrityError):
			chamado = Chamado.objects.create(usuario=usuario, setor=None, grupo_servico=grupo, servico=servico,
										 ramal="4813", assunto="pau no relatório",descricao="copiei texto do editor do "
													"SPL e colei em nova proposição mas quando vou imprimir aparecem "
																			"caracteres estranhos e não imprime PDF.")

	def test_chamado_insere_grupo_nulo(self):
		usuario = User.objects.get(pk=1)
		setor = SetorChamado.objects.get(pk=1)
		servico = Servico.objects.get(pk=1)

		with self.assertRaises(IntegrityError):
			chamado = Chamado.objects.create(usuario=usuario, setor=setor, grupo_servico=None, servico=servico,
										 ramal="4813", assunto="pau no relatório",descricao="copiei texto do editor do "
													"SPL e colei em nova proposição mas quando vou imprimir aparecem "
																			"caracteres estranhos e não imprime PDF.")

	def test_chamado_insere_servico_nulo(self):
		usuario = User.objects.get(pk=1)
		setor = SetorChamado.objects.get(pk=1)
		grupo = GrupoServico.objects.get(pk=1)

		with self.assertRaises(IntegrityError):
			chamado = Chamado.objects.create(usuario=usuario, setor=setor, grupo_servico=grupo, servico=None,
										 ramal="4813", assunto="pau no relatório",descricao="copiei texto do editor do "
													"SPL e colei em nova proposição mas quando vou imprimir aparecem "
																			"caracteres estranhos e não imprime PDF.")

class SetorChamadoTestCase(TestCase):
	fixtures = ['setor_chamado.json']

	def setUp(self):
		super(SetorChamadoTestCase, self).setUp()

'''
	def test_setor_chamado_ok(self):
		setor_chamado = SetorChamado.objects.get(pk=1)
		self.assertEqual(setor_chamado.setor.set_nome, 'Divisão de Desenvolvimento De Sistemas')
'''		

	def test_setor_chamado_setor_nulo(self):
		with self.assertRaises(IntegrityError):
			setor_chamado = SetorChamado.objects.create(setor=None, recebe_chamados=True)

'''					
	def test_setor_chamado_setor_unico(self):
		with self.assertRaises(IntegrityError):
			vsetor = VSetor.objects.get(pk=171)
			setor_chamado = SetorChamado.objects.create(setor=vsetor, recebe_chamados=True)
'''			

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

class ServicoTestCase(TestCase):
	fixtures = ['setor_chamado.json', 'grupo_servico.json', 'servico.json']

	def setUp(self):
		super(ServicoTestCase, self).setUp()			

	def test_servico_ok(self):
		servico = Servico.objects.get(pk=1)
		self.assertEqual(servico.descricao,'Correção de Bug')

	def test_servico_grupo_vazio(self):
		with self.assertRaises(IntegrityError):
			servico = Servico.objects.create(descricao='grupo vazio. tem que dar erro')

	def test_servico_descricao_maior_300(self):
		grupo_servico = GrupoServico.objects.get(pk=1)
		with self.assertRaises(DataError):
			servico = Servico.objects.create(grupo_servico=grupo_servico, descricao='1'*301)

	def test_servico_descricao_vazio(self):
		grupo_servico = GrupoServico.objects.get(pk=1)
		with self.assertRaises(IntegrityError):
			servico = Servico.objects.create(grupo_servico=grupo_servico, descricao=None)

class FilaChamadosTestCase(TestCase):
	fixtures = ['user.json','chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json', 'chamado.json', 'fila_chamados.json']

	def setUp(self):
		super(FilaChamadosTestCase, self).setUp()			

	def test_init(self):
		self.assertEqual(1, 1)
'''
	def test_insere_fila_ok(self):
		usuario = User.objects.get(pk=1)
		chamado = Chamado.objects.get(pk=2)
		fila = FilaChamados.objects.atende(usuario=usuario, chamado=chamado)
		self.assertEqual(fila.chamado.usuario.pk, 1)
		self.assertEqual(chamado.status, 'ATENDIMENTO')
'''

'''			
	def test_insere_fila_usuario_nulo(self):
		chamado = Chamado.objects.get(pk=2)
		with self.assertRaises(ValueError):
			fila = FilaChamados.objects.atende(usuario=None, chamado=chamado)
'''			
'''				
	def test_insere_fila_chamado_nulo(self):
		usuario = User.objects.get(pk=1)
		with self.assertRaises(ValueError):
			fila = FilaChamados.objects.atende(usuario=usuario, chamado=None)
'''
'''
	def test_insere_fila_chamado_atendido(self):
		usuario = User.objects.get(pk=1)
		chamado = Chamado.objects.get(pk=1)
		self.assertEqual(chamado.status, 'ATENDIMENTO')
		with self.assertRaises(ValueError):
			fila = FilaChamados.objects.atende(usuario=usuario, chamado=chamado)
'''

class ChamadoRespostaTestCase(TestCase):
	fixtures = ['user.json','chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json', 'chamado.json', 'fila_chamados.json']

	def setUp(self):
		super(ChamadoRespostaTestCase, self).setUp()			

	def test_init(self):
		self.assertEqual(1, 1)		

	def test_insere_resposta_ok(self)	:
		usuario = User.objects.get(pk=1)
		chamado = Chamado.objects.get(pk=2)
		resposta = ChamadoResposta.objects.create(usuario=usuario, chamado=chamado, resposta='O cabo estava desconectado. Tudo OK.')
		self.assertEqual(resposta.chamado.pk, chamado.pk)

	def test_insere_resposta_usuario_nulo(self)	:
		chamado = Chamado.objects.get(pk=2)
		with self.assertRaises(IntegrityError):
			resposta = ChamadoResposta.objects.create(usuario=None, chamado=chamado, resposta='O cabo estava desconectado. Tudo OK.')

	def test_insere_resposta_nula(self)	:
		usuario = User.objects.get(pk=1)
		chamado = Chamado.objects.get(pk=2)
		with self.assertRaises(IntegrityError):
			resposta = ChamadoResposta.objects.create(usuario=usuario, chamado=chamado, resposta=None)

	def test_insere_resposta_chamado_nulo(self)	:
		usuario = User.objects.get(pk=1)
		with self.assertRaises(IntegrityError):
			resposta = ChamadoResposta.objects.create(usuario=usuario, chamado=None, resposta='O cabo estava desconectado. Tudo OK.')
