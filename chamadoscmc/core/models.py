# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from datetime import datetime

from autentica.models import User as Usuario
#---------------------------------------------------------------------------------------------
# Model para a view V_SETOR
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class AtivosVSetorManager(models.Manager):
    def get_queryset(self):
        return super(AtivosVSetorManager, self).get_queryset().filter(set_ativo = True)

@python_2_unicode_compatible
class VSetor(models.Model):
	class Meta:
		verbose_name_plural = 'Setores'
		managed = False
		db_table = "v_setor"
		ordering = ('set_nome', )

	set_id = models.IntegerField(primary_key=True)
	set_nome = models.CharField(max_length=500)
	set_sigla = models.CharField(max_length=100)
	set_id_superior = models.IntegerField(blank=True, null=True)
	set_ativo = models.BooleanField()
	set_tipo = models.CharField(max_length=1)

	objects = AtivosVSetorManager()

	def __unicode__(self):
		return self.set_nome

	def __str__(self):
		return self.set_nome

#---------------------------------------------------------------------------------------------
# Model SetorChamado
#---------------------------------------------------------------------------------------------
@python_2_unicode_compatible
class SetorChamado(models.Model):
	class Meta:
		verbose_name_plural = 'Setores Chamados'

	setor = models.OneToOneField(VSetor, to_field='set_id', db_constraint=False)
	recebe_chamados = models.BooleanField(default=False)

	def __unicode__(self):
		return self.setor.set_nome

	def __str__(self):
		return self.setor.set_nome

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

	def clean(self):
		if self.grupo_servico.patrimonio_obrigatorio:
			if self.patrimonio == '' or self.patrimonio == None:
				raise ValidationError('Patrimônio obrigatório para ' + self.grupo_servico.descricao)

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return 'usuario:%s ' \
			   'setor:%s ' \
			   'grupo_servico:%s ' \
			   'servico:%s ' \
			   'ramal:%s ' \
			   'data_abertura:%s' % (str(self.usuario),
									 str(self.setor),
									 str(self.grupo_servico),
									 str(self.servico),
									 str(self.ramal),
									 str(self.data_abertura))


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