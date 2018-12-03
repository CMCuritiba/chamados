from django.template import Context
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from consumer.lib.helper import ServiceHelper
from django.conf import settings

from chamadoscmc.core.models import ChamadoAssinatura

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

        s_helper = ServiceHelper()

        assunto = 'CMC - Controle de Chamados'
        para = [chamado.usuario.email]

        #de = 'chamados@cmc.pr.gov.br'
        de = 'Sistema de Chamados <no-reply@cmc.pr.gov.br>'

        link = getattr(settings, 'SERVER_NAME', 'https://chamados.staging.cmc.pr.gov.br/')

        respostas = chamado.chamadoresposta_set.all().order_by('data')

        try:
            ultima_resposta = chamado.chamadoresposta_set.latest('id')
        except:
            ultima_resposta = ''

        if chamado.setor_solicitante is not None:
            setor = s_helper.get_setor(chamado.setor_solicitante)
            setor_solicitante = setor.set_nome
        else:
            setor_solicitante = ''

        messages = []
        ctx = {
            'chamado_id': chamado.id,
            'usuario': chamado.usuario.username,
            'data_abertura': chamado.data_abertura,
            'setor': chamado.setor.get_nome(),
            'grupo_servico': chamado.grupo_servico,
            'servico': chamado.servico,
            'assunto': chamado.assunto,
            'status': chamado.status,
            'resposta': ultima_resposta,
            'respostas': respostas,
            'link': link,
            'setor_solicitante': setor_solicitante
        }
        mensagem_template = get_template('fila/email.txt').render(Context(ctx))
        message = EmailMessage(assunto, mensagem_template, to=para, from_email=de)
        #message.content_subtype = 'text'
        messages.append(message)

        #cria emails para as assinaturas
        assinaturas = ChamadoAssinatura.objects.filter(chamado=chamado)
        para = []
        mensagem_template = get_template('fila/email_assinado.txt').render(Context(ctx))
        for assinatura in assinaturas:
            para.append(assinatura.email)

        message = EmailMessage(assunto, mensagem_template, to=para, from_email=de)
        messages.append(message)

        return messages

