# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

class CustomUserAdmin(UserAdmin):
	model = User
	actions = None

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def get_readonly_fields(self, request, obj=None):
		retorno = ['username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'lotado', 'matricula', 'chefia','is_superuser','last_login','password']
		
		return retorno

	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('lotado', 'matricula', 'chefia',)}),
	)
	list_per_page = 20
	ordering = ('username', 'lotado')
	search_fields = ('username', )
	list_filter = ('lotado', )

admin.site.register(User, CustomUserAdmin)