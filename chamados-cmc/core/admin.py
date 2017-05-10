# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Setor

class SetorAdmin(admin.ModelAdmin):
	model = Setor
	actions = None

	list_display = ('descricao', 'recebe_chamados')
	list_per_page = 20
	ordering = ('descricao', )
	search_fields = ('descricao', )

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return self.readonly_fields + ('descricao', 'id_elotech')
		return self.readonly_fields

admin.site.register(Setor, SetorAdmin)