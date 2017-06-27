from __future__ import with_statement
from fabric.api import abort, local, task, run, local, env, cd, sudo, prefix
from fabric.colors import red, green
from contextlib import contextmanager
import os  


PROJECT_NAME = 'chamados'
WEBAPPS = '/usr/share/webapps'
HTML = '/var/www/html'
ENVS = '/usr/share/envs'
PROJECT_ROOT = WEBAPPS + '/%s' % PROJECT_NAME
REPO = 'https://github.com/CMCuritiba/chamados.git'
USERAPP = 'cmc-apps'
ENV_NAME = 'chamados'

env.hosts = []

@task
def localhost():
	env.hosts = ['localhost']
	env.environment = 'localhost'
	env.virtualenv = '/home/alexandre.odoni/personal/python/env-chamados-cmc/'
	env.activate = '/bin/bash /home/alexandre.odoni/personal/python/env-chamados-cmc/bin/activate'

@task
def staging():
	env.hosts = ['staging.cmc.pr.gov.br']
	env.environment = 'staging'	
	env.user = 'suporte'
	env.virtualenv = '/usr/share/envs/{}'.format(ENV_NAME)
	env.activate = 'source /usr/share/envs/{}/bin/activate'.format(ENV_NAME)
	env.wwwdata = 'www-data'
	env.python_location = '/usr/bin/python3.4'

@task
def production():
	env.hosts = []
	env.environment = 'production'	
	env.user = 'www-data'
	env.virtualenv = ''
	env.activate = ''

# ---------------------------------------------------------------------------------------------------------------
# NÃO MUDE NADA ABAIXO !!!!!!!
# ---------------------------------------------------------------------------------------------------------------

def cria_grupo():
	sudo('addgroup --system {}'.format(USERAPP))

def cria_userapp():
	sudo('adduser --system --ingroup {} --home /usr/share/webapps --disabled-login {}'.format(USERAPP, USERAPP))

def clean():
	''' Limpa Python bytecode '''
	sudo('find . -name \'*.py?\' -exec rm -rf {} \;')

def chown():
	''' Seta permissões ao usuário/grupo corretos '''
	sudo('chown -R {}:{} {}'.format(USERAPP, USERAPP, PROJECT_ROOT))
	sudo('chown -R {}:{} {}'.format(USERAPP, USERAPP, ENVS))
	sudo('chown -R {}:{} {}'.format(USERAPP, env.wwwdata, HTML + '/' + PROJECT_NAME))	

def cria_webapps():
	sudo('mkdir -p {}'.format(WEBAPPS))
	sudo('mkdir -p {}'.format(PROJECT_ROOT))
	#sudo('chown -R {}:{} {}'.format(USERAPP, USERAPP, WEBAPPS))

def cria_envs():
	sudo('mkdir -p {}'.format(ENVS))
	#sudo('chown -R {}:{} {}'.format(USERAPP, USERAPP, ENVS))

def cria_html():
	sudo('mkdir -p {}'.format(HTML))
	sudo('mkdir -p {}'.format(HTML + '/' + PROJECT_NAME))
	sudo('mkdir -p {}'.format(HTML + '/' + PROJECT_NAME + '/logs'))
	#sudo('chown -R {}:{} {}'.format(USERAPP, env.wwwdata, HTML + '/' + PROJECT_NAME))	

def restart():
	sudo('supervisorctl reread')
	sudo('supervisorctl reload')
	sudo('service memcached restart')
	sudo('service nginx restart')

@contextmanager
def source_virtualenv():
	with prefix(env.activate):
		yield

@task
def testa_local():
	local('clear')
	result = local("./manage.py test --settings=config.settings.test")
	if result.failed:
		print(red("Algum teste falhou", bold=True))
	else:
		print(green("Todos testes passaram. Pronto para atualizar git "))

@task
def verifica():
	with cd(PROJECT_ROOT):	
		with source_virtualenv():
			run('./manage.py check --settings=config.settings.production')

@task
def pull_master():
	with cd(PROJECT_ROOT):
		run('git pull origin master')

@task
def install_production():
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			''' Ativa o ambiente virtual '''
			run(env.activate)

			''' Instala todos os pacotes no servidor '''
			sudo('pip install -r requirements/production.txt')	


@task
def bootstrap():
	# Atualiza código para o servidor de aplicação

	# git, nginx, supervisor e memcached
	sudo('aptitude update')
	sudo('aptitude install git')
	sudo('aptitude install supervisor')
	sudo('aptitude install nginx')
	sudo('aptitude install memcached')
	# bibliotecas diversas usadas pelo projeto (ldap, xmlm, ssl, etc) 
	sudo('aptitude install libpq-dev')
	sudo('aptitude install python-dev')
	#sudo('apt-get install python3.5-dev')
	sudo('aptitude install python3.4-dev')
	sudo('aptitude install python-pip')
	sudo('aptitude install python-virtualenv')
	sudo('aptitude install libfreetype6-dev')
	sudo('aptitude install libncurses5-dev')
	sudo('aptitude install libxml2-dev')
	sudo('aptitude install libxslt1-dev')
	sudo('aptitude install zlib1g-dev')
	sudo('aptitude install libffi-dev')
	sudo('aptitude install libsasl2-dev')
	sudo('aptitude install libldap2-dev')
	sudo('aptitude install libssl-dev')
	# Para python 3.4 necessário bibliotecas abaixo:
	sudo('aptitude install libpcap0.8-dev')
	sudo('aptitude install python3-setuptools')
	sudo('aptitude install libjpeg62-turbo-dev')

	sudo('aptitude install curl')
	# baixar o node e instalar
	# sudo('curl -sL https://deb.nodesource.com/setup_6.x | bash -')
	# sudo('aptitude install -y nodejs')
	# sudo('npm install -g bower')

	# Cria os diretórios e permissões necessários 

	cria_grupo()
	cria_userapp()
	cria_webapps()	
	cria_envs()
	cria_html()
	sudo('git clone {} {}'.format(REPO, PROJECT_ROOT))

	with cd(PROJECT_ROOT):
		# Cria o ambiente virtual do projeto 
		sudo('virtualenv --python={} {}'.format(env.python_location, env.virtualenv))

		with source_virtualenv():
			# Ativa o ambiente virtual 
			sudo(env.activate, user='cmc-apps')

			# Instala todos os pacotes no servidor 
			sudo('pip install -r requirements/production.txt')

	# Acerta o usuário/grupo
	chown()

@task
def manage_collectstatic():
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Gera todos os arquivos css/js
			sudo('python manage.py collectstatic --settings=config.settings.production', user='cmc-apps')

@task
def git_update():
	with cd(PROJECT_ROOT):
		# Atualiza servidor com última versão do master
		sudo('git pull origin master', user='cmc-apps')

@task 
def cria_links():
	sudo('ln -sf {}/deploy/staging/supervisor.conf /etc/supervisor/conf.d/mscmc.conf'.format(PROJECT_ROOT))
	sudo('ln -sf {}/deploy/staging/nginx.conf /etc/nginx/sites-enabled/mscmc'.format(PROJECT_ROOT))
	sudo('chmod a+x {}/deploy/staging/run.sh'.format(PROJECT_ROOT))

@task
def restart_nginx_supervisor():
	sudo('supervisorctl reload')
	sudo('supervisorctl restart {}'.format(ENV_NAME))
	sudo('service nginx restart')	