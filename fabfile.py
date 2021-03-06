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
USERAPP = 'www-data'
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
	env.python_location = '/usr/bin/python3.5'

@task
def production():
	env.hosts = ['sucupira.cmc.pr.gov.br']
	env.environment = 'production'	
	env.user = 'suporte'
	env.virtualenv = '/usr/share/envs/{}'.format(ENV_NAME)
	env.activate = 'source /usr/share/envs/{}/bin/activate'.format(ENV_NAME)
	env.wwwdata = 'www-data'
	env.python_location = '/usr/bin/python3.5'

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

def des_chown():
	''' Seta permissões ao usuário/grupo corretos '''
	sudo('chown -R {} {}'.format(env.user, PROJECT_ROOT))
	sudo('chown -R {} {}'.format(env.user, ENVS))
	sudo('chown -R {} {}'.format(env.user, HTML + '/' + PROJECT_NAME))	

def cria_webapps():
	sudo('mkdir -p {}'.format(WEBAPPS))
	sudo('mkdir -p {}'.format(PROJECT_ROOT))
	sudo('chown -R {}:{} {}'.format(USERAPP, USERAPP, WEBAPPS))

def cria_envs():
	sudo('mkdir -p {}'.format(ENVS))
	#sudo('chown -R {}:{} {}'.format(USERAPP, USERAPP, ENVS))

def cria_html():
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
	sudo('apt-get update')
	sudo('apt-get install git')
	sudo('apt-get install supervisor')
	sudo('apt-get install nginx')
	sudo('apt-get install memcached')
	# bibliotecas diversas usadas pelo projeto (ldap, xmlm, ssl, etc) 
	sudo('apt-get install libpq-dev')
	sudo('apt-get install python-dev')
	sudo('apt-get install python3.5-dev')
	#sudo('apt-get install python3.4-dev')
	sudo('apt-get install python-pip')
	sudo('apt-get install python-virtualenv')
	sudo('apt-get install libfreetype6-dev')
	sudo('apt-get install libncurses5-dev')
	sudo('apt-get install libxml2-dev')
	sudo('apt-get install libxslt1-dev')
	sudo('apt-get install zlib1g-dev')
	sudo('apt-get install libffi-dev')
	sudo('apt-get install libsasl2-dev')
	sudo('apt-get install libldap2-dev')
	sudo('apt-get install libssl-dev')
	# Para python 3.4 necessário bibliotecas abaixo:
	sudo('apt-get install libpcap0.8-dev')
	sudo('apt-get install python3-setuptools')
	sudo('apt-get install libjpeg62-turbo-dev')

	sudo('apt-get install curl')
	# baixar o node e instalar
	sudo('curl -sL https://deb.nodesource.com/setup_8.x | bash -')
	sudo('apt-get install -y nodejs')
	sudo('npm install -g bower')

	#instalar bibliotecas do libreoffice para geracao de documentos
	sudo('apt-get install libreoffice-core')
	sudo('apt-get install libreoffice-writer')

	# Cria os diretórios e permissões necessários 

	#cria_grupo()
	#cria_userapp()
	cria_webapps()	
	cria_envs()
	cria_html()
	sudo('git clone {} {}'.format(REPO, PROJECT_ROOT))
	
	with cd(PROJECT_ROOT):
		# Cria o ambiente virtual do projeto 
		sudo('virtualenv --python={} {}'.format(env.python_location, env.virtualenv))

		with source_virtualenv():
			# Ativa o ambiente virtual 
			run(env.activate)

			# Instala todos os pacotes no servidor 
			sudo('pip install -r requirements/production.txt')

	# Acerta o usuário/grupo
	chown()

@task
def manage_bower():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			run('./manage.py bower_install --settings=config.settings.production')
	chown()

@task
def manage_collectstatic():
	chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Gera todos os arquivos css/js
			sudo('./manage.py collectstatic --noinput --clear --settings=config.settings.production', user=USERAPP)

@task
def git_update():
	with cd(PROJECT_ROOT):
		# Atualiza servidor com última versão do master
		#des_chown()
		#cria_webapps()
		#sudo('git clone {} {}'.format(REPO, PROJECT_ROOT))
		sudo('git pull origin master')
		if env.environment == 'staging':
			sudo('chmod a+x {}/deploy/staging/run.sh'.format(PROJECT_ROOT))
		elif env.environment == 'production':
			sudo('chmod a+x {}/deploy/production/run.sh'.format(PROJECT_ROOT))
		else:
			print('Nenhum ambiente selecionado. Defina staging ou production.')

@task 
def cria_links():
	if env.environment == 'staging' or env.environment == 'production':
		sudo('ln -sf {}/deploy/{}/supervisor.conf /etc/supervisor/conf.d/chamados_cmc.conf'.format(PROJECT_ROOT,env.environment))
		sudo('ln -sf {}/deploy/{}/nginx.conf /etc/nginx/sites-enabled/chamados_cmc'.format(PROJECT_ROOT,env.environment))
		sudo('chmod a+x {}/deploy/{}/run.sh'.format(PROJECT_ROOT,env.environment))
	else:
		print('Nenhum ambiente selecionado. Defina staging ou production.')

@task
def restart_nginx_supervisor():
	#sudo('supervisorctl reload')
	sudo('supervisorctl stop celery')
	# ainda não foi resolvido no celery processo para matar os filhos via supervisor
	# só mata o processo 'pai', deixando os filhos zumbis
	# o comando abaixo detona os zumbis na mão
	sudo('pkill -f {}'.format('/usr/share/envs/chamados/bin/celery'))
	sudo('supervisorctl reread')
	sudo('supervisorctl restart {}'.format(PROJECT_NAME))
	sudo('supervisorctl start celery')
	sudo('service nginx restart')

@task
def manage_makemigrations():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			run('./manage.py makemigrations --settings=config.settings.production')
			#run('./manage.py makemigrations autentica --settings=config.settings.production')
			#run('./manage.py makemigrations cadastro --settings=config.settings.production')
	chown()	

@task
def manage_migrate():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			run('./manage.py migrate --settings=config.settings.production')
			#run('./manage.py migrate autentica --settings=config.settings.production')
			#run('./manage.py migrate cadastro --settings=config.settings.production')
	chown()		

@task
def carga_inicial_bd():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Gera todos os arquivos css/js
			#sudo('./manage.py flush --settings=config.settings.production', user=USERAPP)
			sudo('./manage.py carga_inicial --palavra_magica=ZACA --settings=config.settings.production', user=USERAPP)
	chown()		

@task
def update_autenticacao():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			sudo('pip install https://github.com/CMCuritiba/django-cmcldapauth/raw/master/dist/django-cmcldapauth-0.3.tar.gz --upgrade --no-cache-dir')
			#run('python manage.py makemigrations votacao --settings=config.settings.production')
			#run('./manage.py makemigrations autentica --settings=config.settings.production')
			#run('./manage.py makemigrations cadastro --settings=config.settings.production')
	chown()			

@task
def update_consumer():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			sudo('pip install https://github.com/CMCuritiba/django-cmc-consumer/blob/master/dist/django-cmc-consumer-0.2.tar.gz?raw=true --upgrade --no-cache-dir')
			#run('python manage.py makemigrations votacao --settings=config.settings.production')
			#run('./manage.py makemigrations autentica --settings=config.settings.production')
			#run('./manage.py makemigrations cadastro --settings=config.settings.production')
	chown()	

@task
def pip_templated():
	sudo('apt-get install libreoffice-core')
	sudo('apt-get install libreoffice-writer')
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			sudo('pip install templated-docs')
			#run('python manage.py makemigrations votacao --settings=config.settings.production')
			#run('./manage.py makemigrations autentica --settings=config.settings.production')
			#run('./manage.py makemigrations cadastro --settings=config.settings.production')
	chown()				

@task
def manage_sequence():
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			# Roda o bower install
			run('./manage.py sqlsequencereset core --settings=config.settings.production')
			#run('./manage.py makemigrations autentica --settings=config.settings.production')
			#run('./manage.py makemigrations cadastro --settings=config.settings.production')
	chown()		

@task
def instala_report():	
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			sudo('pip install django-easy-pdf')
			sudo('pip install https://github.com/CMCuritiba/django-cmc-report/blob/master/dist/django-cmc-report-0.1.tar.gz?raw=true')
	chown()				

@task
def atualiza_django():	
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			sudo('pip install --upgrade Django==1.11.18')
			#sudo('pip install --upgrade django-python3-ldap')
			#sudo('pip install --upgrade django-ldapdb')
	chown()					

@task
def atualiza_django_ldap():	
	des_chown()
	with cd(PROJECT_ROOT):
		with source_virtualenv():
			sudo('pip install --upgrade django-python3-ldap')
			sudo('pip install --upgrade django-ldapdb')
	chown()						