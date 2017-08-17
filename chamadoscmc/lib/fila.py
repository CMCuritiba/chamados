# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from datetime import datetime

from autentica.models import User as Usuario
from chamadoscmc.core.models import GrupoServico, Servico, Chamado, FilaChamados, ChamadoResposta, HistoricoChamados, SetorChamado
from chamadoscmc.lib.mail import envia_email


def enviaEmail(function):
	def wrap(*args, **kwargs):
		retorno = function(*args, **kwargs)
		envia_email(args[2])
		return retorno
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__

	return wrap

def novidade(function):
	def wrap(*args, **kwargs):
		chamado = args[2]
		chamado.novidade = True
		return function(*args, **kwargs)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__

	return wrap


class FilaManager(object):

	@novidade
	#@enviaEmail
	@transaction.atomic
	def atende(self, usuario, chamado):
		if chamado == None or chamado.status != 'ABERTO':
			raise ValueError('Status do chamado não é ABERTO.')
		if usuario == None:
			raise ValueError('Usuário inválido')
		fila = FilaChamados.objects.filter(chamado=chamado).first()
		if fila == None:
			fila = FilaChamados.objects.create(usuario=usuario, chamado=chamado)
		else:
			nuser = Usuario.objects.get(pk=usuario.id)
			fila.chamado = chamado
			fila.usuario = usuario
			fila.save()
		chamado.status = 'ATENDIMENTO'
		chamado.save()
		historico = HistoricoChamados.objects.create(chamado=chamado, status='ATENDIMENTO', usuario=usuario)
		return fila

	@novidade
	#@enviaEmail
	@transaction.atomic
	def devolve(self, usuario, chamado):
		print('0000000000000000000000000')
		if chamado == None or chamado.status != 'ATENDIMENTO':
			raise ValueError('Status do chamado não é ATENDIMENTO.')
		fila = FilaChamados.objects.filter(chamado=chamado).first()
		fila.usuario = None
		fila.save()
		chamado.status = 'ABERTO'
		chamado.save()
		historico = HistoricoChamados.objects.create(chamado=chamado, status='ABERTO')
		print('111111111111111111111111111')
		print('22222222222222222222222')
		return fila

	@novidade
	#@enviaEmail
	@transaction.atomic
	def fecha(self, usuario, chamado):
		if chamado == None or chamado.status != 'ATENDIMENTO':
			raise ValueError('Status do chamado não é ATENDIMENTO.')
		chamado.status = 'FECHADO'
		chamado.data_fechamento = datetime.now()
		chamado.save()
		historico = HistoricoChamados.objects.create(chamado=chamado, status='FECHADO', usuario=usuario)
		return None

	@novidade
	#@enviaEmail
	@transaction.atomic
	def reabre(self, usuario, chamado):
		if chamado == None or chamado.status != 'FECHADO':
			raise ValueError('Status do chamado não é FECHADO.')
		fila = FilaChamados.objects.filter(chamado=chamado).first()
		fila.usuario = None
		fila.save()
		chamado.status = 'ABERTO'
		chamado.data_fechamento = None
		chamado.save()
		historico = HistoricoChamados.objects.create(chamado=chamado, status='ABERTO')
		return fila

	@transaction.atomic
	def cria(self, usuario, chamado):
		if chamado == None:
			raise ValueError('Chamado inválido')
		fila = FilaChamados.objects.filter(chamado=chamado).first()
		if fila == None:
			fila = FilaChamados.objects.create(usuario=usuario, chamado=chamado)
		else:
			fila.chamado = chamado
			fila.usuario = usuario
			fila.save()
		return fila