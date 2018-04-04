from factory.django import DjangoModelFactory

from .. import models
from autentica.models import User as Usuario

class SetorChamadoFactory(DjangoModelFactory):
	class Meta:
		model = models.SetorChamado

	id = 1
	setor_id = 171
	recebe_chamados = True
	localizacao = False

class ServicoFactory(DjangoModelFactory):
	class Meta:
		model = models.Servico

class GrupoServicoFactory(DjangoModelFactory):
	class Meta:
		model = models.GrupoServico		

class UsuarioFactory(DjangoModelFactory):
	class Meta:
		model = Usuario

