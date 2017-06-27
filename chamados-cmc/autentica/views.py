# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django import forms
from django.db import connection, transaction
from ..lib.msconsumer import Pessoa, MSCMCConsumer

import urllib
import environ

def loga(request):
	next = request.GET.get('next')
	context = {'next': next}
	#return render_to_response('autentica/login.html', context_instance=RequestContext(request, {'next': next}))	
	return render(request, 'autentica/login.html', context)

def valida_usuario(request):
	if request.method == 'POST':
		usuario = request.POST.get('usuario')
		senha = request.POST.get('senha')
		next = request.POST.get('next')
		user = authenticate(username=usuario, password=senha)
		if user is not None:
			if user.is_active:
				login(request, user)
				atualiza(user)
				if next != None and next != 'None':
					return HttpResponseRedirect(next)
				return render_to_response('index.html', context_instance=RequestContext(request))
			else:
				messages.add_message(request, messages.ERROR, "Usuário válido mas desebilitado.")
				return redirect('/autentica/loga/?next=' + next)
		else:
			messages.add_message(request, messages.ERROR, "Usuário ou senha incorretos.")
			return redirect('/autentica/loga/?next=' + next) 

def sair(request):
	logout(request)
	return HttpResponseRedirect('/autentica/loga/?next=/')			

# ----------------------------------------------------------------------------------------------------------------
# Atualiza setor do usuario de acordo com servico elotech
# ----------------------------------------------------------------------------------------------------------------
def atualiza(usuario):
	cons = MSCMCConsumer()
	pessoa = cons.consome_pessoa(usuario.matricula)
	usuario.lotado=pessoa.set_id
	usuario.save()

def index(request):
	print('INDEX')