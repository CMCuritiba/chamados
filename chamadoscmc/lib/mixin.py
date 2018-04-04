# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from braces import views
from django.http import HttpResponseRedirect, HttpResponse

from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired
from ..core.models import SetorChamado

#----------------------------------------------------------------------------------------------
#
#----------------------------------------------------------------------------------------------
class ChamadosAdminRequired(CMCLoginRequired, CMCAdminLoginRequired):
	message_url = '/acesso/admin'

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			return HttpResponseRedirect(self.message_url)

		return super(CMCAdminLoginRequired, self).dispatch(
			request, *args, **kwargs)

#----------------------------------------------------------------------------------------------
#
#----------------------------------------------------------------------------------------------
class ChamadosAtendenteRequired(CMCLoginRequired):
	message_url = '/acesso/atendente'

	def dispatch(self, request, *args, **kwargs):

		setor_chamado = SetorChamado.objects.get(setor_id=request.session['setor_id'])
		if not setor_chamado.recebe_chamados:
			return HttpResponseRedirect(self.message_url)

		return super(CMCLoginRequired, self).dispatch(request, *args, **kwargs)