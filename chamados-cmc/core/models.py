# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Setor(models.Model):
	class Meta:
		verbose_name_plural = 'Setores'

	descricao = models.CharField(max_length=300)
	id_elotech = models.IntegerField(unique=True)
	recebe_chamados = models.BooleanField(default=False)

	def __unicode__(self):
		return self.descricao

	def __str__(self):
		return self.descricao