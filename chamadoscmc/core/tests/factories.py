from factory.django import DjangoModelFactory

from .. import models

class SetorChamadoFactory(DjangoModelFactory):
	class Meta:
		model = models.SetorChamado

	id = 1
	setor_id = 171
	recebe_chamados = True
	localizacao = False