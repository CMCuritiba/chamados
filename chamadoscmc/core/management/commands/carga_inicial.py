# -*- coding: utf-8 -*-
"""
Script que executa carga inicial no BD de chamados
Não execute este script sem ter absoluta certeza do que estiver fazendo
"""

import sys
from django.core.management.base import BaseCommand
from chamadoscmc.core.tests.factories import SetorChamadoFactory, GrupoServicoFactory, ServicoFactory

class Command(BaseCommand):
	help = "Carga inicial no BD de Chamados"

	def add_arguments(self, parser):
		parser.add_argument('--palavra_magica')

	def popula_setor_chamado(self):
		self.stdout.write('...populando SetorChamado')
		SetorChamadoFactory.create(id=1, setor_id=172, recebe_chamados=True, localizacao=False)
		#SetorChamadoFactory.create(id=2, setor_id=171, recebe_chamados=False, localizacao=False)

	def popula_grupo_servico(self):
		self.stdout.write('...populando GrupoServico')		
		GrupoServicoFactory.create(id=1, descricao='Impressora', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=58, descricao='Estação de Trabalho', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=59, descricao='Rede', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=60, descricao='Wi-Fi', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=61, descricao='Libreoffice', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=62, descricao='Sistemas', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=63, descricao='Elotech: Apice/AISE', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=64, descricao='RH Online / Ponto Biométrico', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=65, descricao='Windows virtual', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=66, descricao='Infraestrutura', patrimonio_obrigatorio=False, setor_id=1)
		GrupoServicoFactory.create(id=67, descricao='Outros', patrimonio_obrigatorio=False, setor_id=1)

	def popula_servico(self):
		ServicoFactory.create(id=1, descricao='Troca de tonner', grupo_servico_id=1)
		ServicoFactory.create(id=301, descricao='Não liga', grupo_servico_id=58)
		ServicoFactory.create(id=302, descricao='Usuário não loga', grupo_servico_id=58)
		ServicoFactory.create(id=303, descricao='Reiniciando', grupo_servico_id=58)
		ServicoFactory.create(id=304, descricao='Travando', grupo_servico_id=58)
		ServicoFactory.create(id=305, descricao='Mouse/teclado com defeito', grupo_servico_id=58)
		ServicoFactory.create(id=306, descricao='Monitor não liga', grupo_servico_id=58)
		ServicoFactory.create(id=307, descricao='Monitor desconfigurado', grupo_servico_id=58)
		ServicoFactory.create(id=308, descricao='Não sai áudio', grupo_servico_id=58)
		ServicoFactory.create(id=309, descricao='Criação ou alteração de usuário, senha ou e-mail', grupo_servico_id=59)
		ServicoFactory.create(id=310, descricao='Não acessa ou não aparecem as pastas de rede', grupo_servico_id=59)
		ServicoFactory.create(id=311, descricao='Cota de espaço para pastas de rede', grupo_servico_id=59)
		ServicoFactory.create(id=312, descricao='Cota de espaço para e-mail', grupo_servico_id=59)
		ServicoFactory.create(id=313, descricao='Recuperar backup', grupo_servico_id=59)
		ServicoFactory.create(id=314, descricao='Relatório de navegação na internet', grupo_servico_id=59)
		ServicoFactory.create(id=315, descricao='Não consegue acessar', grupo_servico_id=63)
		ServicoFactory.create(id=316, descricao='Não consegue imprimir', grupo_servico_id=63)
		ServicoFactory.create(id=317, descricao='Nova instalação', grupo_servico_id=63)
		ServicoFactory.create(id=318, descricao='Não imprime', grupo_servico_id=1)
		ServicoFactory.create(id=319, descricao='Impressões manchadas/com falhas', grupo_servico_id=1)
		ServicoFactory.create(id=320, descricao='Cota de impressão', grupo_servico_id=1)
		ServicoFactory.create(id=321, descricao='Relatório de impressões', grupo_servico_id=1)
		ServicoFactory.create(id=323, descricao='Não consegue se conectar', grupo_servico_id=60)
		ServicoFactory.create(id=324, descricao='Não consegue navegar', grupo_servico_id=60)
		ServicoFactory.create(id=325, descricao='Criação de usuário', grupo_servico_id=60)
		ServicoFactory.create(id=327, descricao='Não consegue abrir ou salvar arquivos', grupo_servico_id=61)
		ServicoFactory.create(id=328, descricao='SPL', grupo_servico_id=62)
		ServicoFactory.create(id=329, descricao='SPA', grupo_servico_id=62)
		ServicoFactory.create(id=330, descricao='SAAP', grupo_servico_id=62)
		ServicoFactory.create(id=331, descricao='APL', grupo_servico_id=62)
		ServicoFactory.create(id=332, descricao='Legisladoc', grupo_servico_id=62)
		ServicoFactory.create(id=333, descricao='Não sabe ou não consegue acessar o sistema', grupo_servico_id=64)
		ServicoFactory.create(id=334, descricao='Não abre', grupo_servico_id=65)
		ServicoFactory.create(id=335, descricao='Não acessa pastas de rede', grupo_servico_id=65)
		ServicoFactory.create(id=336, descricao='Não consegue imprimir', grupo_servico_id=65)
		ServicoFactory.create(id=337, descricao='Novo ponto de rede', grupo_servico_id=66)
		ServicoFactory.create(id=338, descricao='Manutenção em ponto de rede', grupo_servico_id=66)
		ServicoFactory.create(id=344, descricao='Travamento', grupo_servico_id=61)

		self.stdout.write('...populando Servico')				

	def popula_localizacao(self):
		self.stdout.write('...populando Localizacao')				

	def popula_pavimento(self):
		self.stdout.write('...populando Pavimento')						

	def handle(self, *args, **options):
		if options['palavra_magica'] != 'ZACA':
			self.stdout.write('##### Você precisa digitar a palavra mágica para executar o script #####')
			sys.exit(1)
		else:
			self.popula_setor_chamado()
			self.popula_grupo_servico()
			self.popula_servico()
			self.popula_localizacao()
			self.popula_pavimento()

			self.stdout.write('Carga completada com sucesso.')				