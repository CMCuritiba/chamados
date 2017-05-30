# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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
