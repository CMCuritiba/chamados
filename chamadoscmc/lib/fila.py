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


class FilaManager(object):

	@transaction.atomic
	def atende(usuario, chamado):
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
		chamado.novidade = True
		chamado.save()
		envia_email(chamado)
		historico = HistoricoChamados.objects.create(chamado=chamado, status='ATENDIMENTO', usuario=usuario)
		historico.save()
		return fila

	@transaction.atomic
	def devolve(usuario, chamado):
		if chamado == None or chamado.status != 'ATENDIMENTO':
			raise ValueError('Status do chamado não é ATENDIMENTO.')
		fila = FilaChamados.objects.filter(chamado=chamado).first()
		fila.usuario = None
		fila.save()
		chamado.status = 'ABERTO'
		chamado.novidade = True
		chamado.save()
		envia_email(chamado)

		historico = HistoricoChamados.objects.create(chamado=chamado, status='ABERTO')
		historico.save()
		return fila

	@transaction.atomic
	def fecha(usuario, chamado):
		if chamado == None or chamado.status != 'ATENDIMENTO':
			raise ValueError('Status do chamado não é ATENDIMENTO.')
		chamado.status = 'FECHADO'
		chamado.novidade = True
		chamado.data_fechamento = datetime.now()
		chamado.save()
		envia_email(chamado)

		historico = HistoricoChamados()
		historico.chamado = chamado
		historico.status = 'FECHADO'
		historico.usuario = usuario
		historico.save()
		return None

	@transaction.atomic
	def reabre(usuario, chamado):
		if chamado == None or chamado.status != 'FECHADO':
			raise ValueError('Status do chamado não é FECHADO.')
		fila = FilaChamados.objects.filter(chamado=chamado).first()
		fila.usuario = None
		fila.save()
		chamado.status = 'ABERTO'
		chamado.novidade = True
		chamado.data_fechamento = None
		chamado.save()
		envia_email(chamado)

		historico = HistoricoChamados.objects.create(chamado=chamado, status='ABERTO')
		historico.save()
		return fila

	@transaction.atomic
	def cria(usuario, chamado):
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