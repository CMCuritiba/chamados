from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage

def envia_email(chamado):
	assunto = 'CMC - Controle de Chanados'
	para = [chamado.usuario.email]
	de = 'telefoniacamara@gmail.com'

	ctx = {
		'chamado_id': chamado.id,
		'usuario': chamado.usuario.username,
		'data_abertura': chamado.data_abertura,
		'setor': chamado.setor.setor,
		'grupo_servico': chamado.grupo_servico,
		'servico': chamado.servico,
		'assunto': chamado.assunto,
		'status': chamado.status,
		'resposta': chamado.chamadoresposta_set.latest('id'),
	}
	mensagem = get_template('fila/email.txt').render(Context(ctx))
			
	EmailMessage(assunto, mensagem, to=para, from_email=de).send()
