# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import GrupoServico, SetorChamado

class GrupoServicoInline(admin.TabularInline):
	model = GrupoServico
	extra = 2
	verbose_name_plural = 'Grupos de Serviço'	

class SetorChamadoAdmin(admin.ModelAdmin):
	model = SetorChamado

	list_display = ('setor',)
	list_per_page = 20
	ordering = ('setor__set_nome', )
	search_fields = ('setor__set_nome', )
	inlines = [GrupoServicoInline]

class GrupoServicoAdmin(admin.ModelAdmin):
	model = GrupoServico
	list_filter = ['setor', ]
	ordering = ('descricao', )
	search_fields = ('descricao', )

admin.site.register(GrupoServico, GrupoServicoAdmin)
admin.site.register(SetorChamado, SetorChamadoAdmin)