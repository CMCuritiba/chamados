import urllib.request
import environ
import simplejson as json
from django.conf import settings


class Pessoa(object):
	def __init__(self, set_id, pes_matricula, pes_nome):	
		self.set_id = set_id
		self.pes_matricula = pes_matricula
		self.pes_nome = pes_nome

class Setor(object):
	def __init__(self, set_id, set_nome, set_sigla, set_id_superior, set_ativo, set_tipo):	
		self.set_id = set_id
		self.set_nome = set_nome
		self.set_sigla = set_sigla
		self.set_id_superior = set_id_superior
		self.set_ativo = set_ativo
		self.set_tipo = set_tipo

# ----------------------------------------------------------------------------------------------------------------
# Classe responsável por consumir as informações JSON 
# ----------------------------------------------------------------------------------------------------------------
class MSCMCConsumer(object):

	def __init__(self):
		self.MSCMC_SERVER = settings.MSCMC_SERVER

	# ----------------------------------------------------------------------------------------------------------------
	# Consome o serviço que retorna dados da pessoa através da matrícula
	# ----------------------------------------------------------------------------------------------------------------
	def consome_pessoa(self, matricula):
		search_url = '{}/api/pessoa/{}/?format=json'.format(self.MSCMC_SERVER, matricula)
		raw = urllib.request.urlopen(search_url)
		js = raw.readlines()
		js_object = json.loads(js[0])
		return Pessoa(js_object['set_id'], js_object['pes_matricula'], js_object['pes_nome'])

	# ----------------------------------------------------------------------------------------------------------------
	# Consome o serviço que retorna dados da pessoa através da matrícula
	# ----------------------------------------------------------------------------------------------------------------
	def consome_setor(self, matricula):
		search_url = '{}/api/setor/{}/?format=json'.format(self.MSCMC_SERVER, matricula)
		raw = urllib.request.urlopen(search_url)
		js = raw.readlines()
		js_object = json.loads(js[0])
		return Setor(js_object['set_id'], js_object['set_nome'], js_object['set_sigla'], js_object['set_id_superior'], js_object['set_ativo'], js_object['set_tipo'])

		