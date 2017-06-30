
from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from ..views import CadastroChamadosIndexView, ChamadoDetailView


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


    def test_index(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = CadastroChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Abertura de Chamados')


    def test_index_table_chamados(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = CadastroChamadosIndexView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Abertura de Chamados')


    def test_detalhe_chamado(self):
        request = self.factory.get('/chamado/')
        request.user = self.user
        response = ChamadoDetailView.as_view()(request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalhes do Chamado')

