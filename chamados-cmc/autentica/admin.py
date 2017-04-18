# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

class CustomUserAdmin(UserAdmin):
	model = User

	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('lotado', 'matricula', 'chefia',)}),
	)
	list_per_page = 20
	ordering = ('username', 'lotado')
	search_fields = ('username', )
	list_filter = ('lotado', )

admin.site.register(User, CustomUserAdmin)