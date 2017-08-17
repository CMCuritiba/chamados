from django.template import Context
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import get_template


class Mailer:
    """
    Send email messages helper class
    """

    def __init__(self, from_email=None):
        # TODO setup the default from email
        self.connection = mail.get_connection()
        self.from_email = from_email

    def send_messages(self, chamado):
        messages = self.__generate_messages(chamado)
        self.__send_mail(messages)

    def __send_mail(self, mail_messages):
        self.connection.open()
        self.connection.send_messages(mail_messages)
        self.connection.close()

    def __generate_messages(self, chamado):

        assunto = 'CMC - Controle de Chamados'
        para = [chamado.usuario.email]
        de = 'chamados@cmc.pr.gov.br'

        try:
            ultima_resposta = chamado.chamadoresposta_set.latest('id')
        except:
            ultima_resposta = ''

        messages = []
        ctx = {
            'chamado_id': chamado.id,
            'usuario': chamado.usuario.username,
            'data_abertura': chamado.data_abertura,
            'setor': chamado.setor.setor,
            'grupo_servico': chamado.grupo_servico,
            'servico': chamado.servico,
            'assunto': chamado.assunto,
            'status': chamado.status,
            'resposta': ultima_resposta,
        }
        mensagem_template = get_template('fila/email.txt').render(Context(ctx))
        message = EmailMessage(assunto, mensagem_template, to=para, from_email=de)
        message.content_subtype = 'html'
        messages.append(message)

        return messages

