# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from braces import views
from django.http import HttpResponseRedirect, HttpResponse

from autentica.util.mixin import CMCLoginRequired, CMCAdminLoginRequired
from ..core.models import SetorChamado, Chamado, FilaChamados

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

		retorno = super(CMCLoginRequired, self).dispatch(request, *args, **kwargs)

		if retorno.status_code == 302:
			return HttpResponseRedirect(retorno.url)

		setor_chamado = SetorChamado.objects.get(setor_id=request.session['setor_id'])
		if not setor_chamado.recebe_chamados:
			return HttpResponseRedirect(self.message_url)

		chave = kwargs.get('pk', None)
		if chave is not None:
			chamado = Chamado.objects.get(pk=chave)
			if chamado.setor != setor_chamado:
				return HttpResponseRedirect(self.message_url)
			try:
				fila = FilaChamados.objects.get(chamado_id=chave)
				if fila.usuario != request.user:
					return HttpResponseRedirect(self.message_url)
			except:
				return HttpResponseRedirect(self.message_url)
		return retorno

#----------------------------------------------------------------------------------------------
#
#----------------------------------------------------------------------------------------------
class ChamadosVisualizaRequired(CMCLoginRequired):
	message_url = '/acesso/atendente'

	def dispatch(self, request, *args, **kwargs):

		retorno = super(CMCLoginRequired, self).dispatch(request, *args, **kwargs)

		if retorno.status_code == 302:
			return HttpResponseRedirect(retorno.url)

		chave = kwargs.get('pk', None)
		if chave is not None:
			chamado = Chamado.objects.get(pk=chave)			

			if chamado.setor_solicitante == request.session['setor_id'] and chamado.usuario == request.user:
				return retorno
			else:
				try:
					setor_chamado = SetorChamado.objects.get(setor_id=request.session['setor_id'])
					if not setor_chamado.recebe_chamados:
						return HttpResponseRedirect(self.message_url)
					else:
						if setor_chamado.setor_id == request.session['setor_id']:
							return retorno
						else:
							return HttpResponseRedirect(self.message_url)	

				except:
					return HttpResponseRedirect(self.message_url)