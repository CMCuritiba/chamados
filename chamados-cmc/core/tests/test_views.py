
from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from ..views import CadastroChamadosIndexView


class ChamadoViewTests(TestCase):
    fixtures = ['user.json', 'chamado.json', 'setor_chamado.json', 'grupo_servico.json', 'servico.json']

    nome_usuario = 'tora'
    senha = 'mandioca'


    def setUp(self):
        self.user = get_user_model().objects.create_user(self.nome_usuario, password=self.senha)
        self.user.is_staff = True
        self.user.save()
        self.factory = RequestFactory()


    def setup_request(self, request):
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.session['some'] = 'some'
        request.session.save()





