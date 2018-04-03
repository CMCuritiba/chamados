# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from braces import views
from django.http import HttpResponseRedirect, HttpResponse

from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired

class ChamadosAdminRequired(CMCLoginRequired, CMCAdminLoginRequired):
	message_url = '/acesso/admin'

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			return HttpResponseRedirect(self.message_url)

		return super(CMCAdminLoginRequired, self).dispatch(
			request, *args, **kwargs)