# -*- coding: utf-8 -*-
"""
Script que executa carga de chamados ja criados no BD de chamados
Não execute este script sem ter absoluta certeza do que estiver fazendo
"""

import sys
from django.core.management.base import BaseCommand
from chamadoscmc.core.tests.factories import SetorChamadoFactory, GrupoServicoFactory, ServicoFactory

class Command(BaseCommand):
	help = "Carga de chamados criados no BD de Chamados"

	def add_arguments(self, parser):
		parser.add_argument('--palavra_magica')

	def popula_chamado(self):
		self.stdout.write('...populando Chamado')		

	def popula_fila_chamado(self):
		self.stdout.write('...populando FilaChamado')				

	def popula_historico_chamado(self):
		self.stdout.write('...populando HistoricoChamado')						

	def popula_chamado_resposta(self):
		self.stdout.write('...populando ChamadoResposta')								

	def popula_chamado_anexo(self):
		self.stdout.write('...populando ChamadoAnexo')								

	def handle(self, *args, **options):
		if options['palavra_magica'] != 'ZACA':
			self.stdout.write('##### Você precisa digitar a palavra mágica para executar o script #####')
			sys.exit(1)
		else:
			self.popula_chamado()
			self.popula_fila_chamado()
			self.popula_historico_chamado()
			self.popula_chamado_resposta()
			self.popula_chamado_anexo()

			self.stdout.write('Carga completada com sucesso.')				