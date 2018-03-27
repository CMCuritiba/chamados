# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from datetime import datetime

from autentica.models import User as Usuario
from consumer.lib.helper import ServiceHelper

#---------------------------------------------------------------------------------------------
# Model Localizacao
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class Localizacao(models.Model):
	class Meta:
		verbose_name_plural = 'Localizações'

	descricao = models.CharField(max_length=300)

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return self.descricao		

#---------------------------------------------------------------------------------------------
# Model Pavimento
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class Pavimento(models.Model):
	class Meta:
		verbose_name_plural = 'Pavimentos'

	localizacao = models.ForeignKey(Localizacao)
	descricao = models.CharField(max_length=300)

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return self.descricao				

#---------------------------------------------------------------------------------------------
# Model SetorChamado
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class SetorChamado(models.Model):
	class Meta:
		verbose_name_plural = 'Setores Chamados'

	#setor = models.OneToOneField(VSetor, to_field='set_id', db_constraint=False)
	setor_id = models.IntegerField(unique=True) # id da elotech
	recebe_chamados = models.BooleanField(default=False)
	localizacao = models.BooleanField(default=False)

	def __unicode__(self):
		service_helper = ServiceHelper()
		setor = service_helper.get_setor(self.setor_id)
		return setor.set_nome

	def __str__(self):
		service_helper = ServiceHelper()
		setor = service_helper.get_setor(self.setor_id)
		return setor.set_nome

	def get_sigla(self):
		service_helper = ServiceHelper()
		setor = service_helper.get_setor(self.setor_id)
		return setor.set_sigla

	def get_nome(self):
		service_helper = ServiceHelper()
		setor = service_helper.get_setor(self.setor_id)
		return setor.set_nome


#---------------------------------------------------------------------------------------------
# Model GrupoServico
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class GrupoServico(models.Model):
	class Meta:
		verbose_name_plural = 'Grupo de Serviços'

	descricao = models.CharField(max_length=300)
	setor = models.ForeignKey(SetorChamado)
	patrimonio_obrigatorio = models.BooleanField(default=False)

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return self.descricao		

#---------------------------------------------------------------------------------------------
# Model Servico
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class Servico(models.Model):
	class Meta:
		verbose_name_plural = 'Serviços'

	descricao = models.CharField(max_length=300)
	grupo_servico = models.ForeignKey(GrupoServico)

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return self.descricao				

#---------------------------------------------------------------------------------------------
# Model Chamado
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class Chamado(models.Model):
	PRIORIDADE_BAIXA = 'BAIXA'
	PRIORIDADE_NORMAL = 'NORMAL'
	PRIORIDADE_ALTA = 'ALTA'
	PRIORIDADE_CHOICES = (
		(PRIORIDADE_BAIXA, 'Baixa'),
		(PRIORIDADE_NORMAL, 'Normal'),
		(PRIORIDADE_ALTA, 'Alta')
	)
	STATUS_ABERTO = 'ABERTO'
	STATUS_ATENDIMENTO = 'ATENDIMENTO'
	STATUS_FECHADO = 'FECHADO'
	STATUS_CHOICES = (
		(STATUS_ABERTO, 'Aberto'),
		(STATUS_ATENDIMENTO, 'Em Atendimento'),
		(STATUS_FECHADO, 'Fechado')
	)
	usuario = models.ForeignKey(Usuario)
	setor = models.ForeignKey(SetorChamado)
	grupo_servico = models.ForeignKey(GrupoServico)
	servico = models.ForeignKey(Servico)
	ramal = models.CharField(max_length=15, null=True, blank=True)
	assunto = models.CharField(max_length=200, null=True, blank=True)
	descricao = models.TextField(null=True, blank=True)
	data_abertura = models.DateTimeField(default=timezone.now, blank=True)
	prioridade = models.CharField(max_length=10, null=False, blank=False, choices=PRIORIDADE_CHOICES,
								  default=PRIORIDADE_NORMAL)
	status = models.CharField(max_length=15, null=False, blank=False, choices=STATUS_CHOICES, default=STATUS_ABERTO)
	data_fechamento = models.DateTimeField(null=True)
	novidade = models.BooleanField(default=False)
	patrimonio = models.CharField(max_length=100, null=True, blank=True)
	localizacao = models.ForeignKey(Localizacao, blank=True, null=True)
	pavimento = models.ForeignKey(Pavimento,  blank=True, null=True)
	setor_solicitante = models.IntegerField(blank=True, null=True)

	'''
	def clean(self):
		data = self.cleaned_data
		print('---------------------------')
		print(data)
		print('---------------------------')
		if self.grupo_servico is None:
			raise ValidationError('Grupo Serviço Obrigatório')
		if self.grupo_servico.patrimonio_obrigatorio:
			if self.patrimonio == '' or self.patrimonio is None:
				raise ValidationError('Patrimônio obrigatório para ' + self.grupo_servico.descricao)
	'''

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return self.descricao

#---------------------------------------------------------------------------------------------
# Model FilaChamados
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class FilaChamados(models.Model):
	class Meta:
		verbose_name_plural = 'Fila de Chamados'

	usuario = models.ForeignKey(Usuario, blank=True, null=True)
	chamado = models.ForeignKey(Chamado)

	def __unicode__(self):
		return self.chamado.assunto

	def __str__(self):
		return self.chamado.assunto

#---------------------------------------------------------------------------------------------
# Model HistoricoChamados
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class HistoricoChamados(models.Model):
	class Meta:
		verbose_name_plural = 'Histórico do Chamado'

	chamado = models.ForeignKey(Chamado)
	data = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=15)
	usuario = models.ForeignKey(Usuario, blank=True, null=True)

	def __unicode__(self):
		return self.chamado.assunto

	def __str__(self):
		return self.chamado.assunto		

#---------------------------------------------------------------------------------------------
# Model ChamadoResposta
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class ChamadoResposta(models.Model):
	class Meta:
		verbose_name_plural = 'Respostas para o Chamado'

	chamado = models.ForeignKey(Chamado)
	data = models.DateTimeField(default=timezone.now)
	usuario = models.ForeignKey(Usuario)
	resposta = models.TextField()

	def __unicode__(self):
		return self.resposta

	def __str__(self):
		return self.resposta

#---------------------------------------------------------------------------------------------
# Model ChamadoAnexo
#---------------------------------------------------------------------------------------------		
class ChamadoAnexo(models.Model):
	chamado = models.ForeignKey(Chamado, related_name='anexos')
	arquivo = models.ImageField(upload_to="imagens")
	uploaded_at = models.DateTimeField(auto_now_add=True)
	descricao = models.CharField(max_length=255, blank=True)