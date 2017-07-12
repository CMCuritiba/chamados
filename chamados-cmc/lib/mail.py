from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

def envia_email(request, chamado):
	assunto = 'CMC - Controle de Chanados'
	para = [chamado.usuario.email]
	de = ''
	ctx = {
		'chamado_id': chamado.id,
		'usuario': chamado.usuario.username,
	}
	mensagem = get_template('fila/email.txt').render(Context(ctx))
			
	EmailMessage(assunto, mensagem, to=para, from_email=de).send()