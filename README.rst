Aplicação Chamados CMC
======================

Aplicação Django para controle de chamados Câmara Municipal de Curitiba

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

.. image:: https://travis-ci.org/CMCuritiba/chamados.svg?branch=master
    :target: https://travis-ci.org/CMCuritiba/chamados

.. image:: https://codecov.io/gh/CMCuritiba/chamados/coverage.svg?branch=master
    :target: https://codecov.io/gh/CMCuritiba/chamados/


:License: MIT


Contribuindo
------------

Escolha o local onde vai armazenar o repositório, por exemplo ~/projetos/python/:

::

    $ mkdir -p ~/projetos/python
    $ cd ~/projetos/python

Membros da equipe da Diretoria de Informática da Câmara Municipal pode seguir as instruções abaixo.
Membros da comunidade devem seguir os passos abaixo:

Crie um fork e clone o repositório:

::

    $ git clone https://github.com/SEU_USUARIO_GITHUB/chamados
    $ cd chamados

Adicione o repositório remoto upstream:

``$ git remote add upstream git@github.com:CMCuritiba/chamados.git``

Após realizar uma contribuição, um pull request pode ser feito diretamente ao branch master.

Os membros da Diretoria de Informática da Câmara Municipal podem clonar o repositório principal, mas devem trabalhar no branch develop.

::

    $ git clone git@github.com:CMCuritiba/chamados.git
    $ cd chamados
    $ git checkout develop

Em caso de dúvidas verifique se o branch está correto, o branch ativo terá um asterisco ao lado do nome:

::

    $ git branch
    master
    develop*

Após realizar uma contribuição, um merge request pode ser feito do branch develop para o branch master.

Ambiente virtual
----------------

É recomendado criar um ambiente virtual.
O ambiente virtual pode ser criado de algumas maneiras.
Seguem dois exemplos, com a biblioteca padrão do python, venv e outro exemplo com a biblioteca virtualenvwrapper.

Para criar um ambiente virtual com a biblioteca venv para o python3 que é a versão de python padrão dos projetos no momento, normalmente fazemos:

::

    $ mkdir -p ~/projetos/python/chamados
    $ cd ~/projetos/python/chamados
    $ python3 -m venv venv
    $ source venv/bin/activate

Sempre que precisar, será necessário repetir o último comando.
Ele serve para ativar o ambiente virtual.
Necessário sempre que uma nova janela de terminal for aberta.
Por exemplo, ao abir um terminal:

::

    $ cd ~/projetos/python/chamados
    $ source venv/bin/activate

Outro modo de criar e utilizar ambientes virtuais é com a biblioteca virtualenvwrapper.
O pacote do virtualenvwrapper deve estar instalado no sistema operacional.
Para instalar em um ambiente similar ao Debian GNU/Linux bastam alguns comandos, atenção essas instruções podem variar um pouco dependendo da distribuição:

::

    $ sudo apt install virtualenvwrapper
    $ source /usr/share/virtualenvwrapper/virtualenvwrapper.sh

Ou então, se preferir, pode utilizar as instruções no link da documentação https://virtualenvwrapper.readthedocs.io/en/latest/install.html

Exemplo de criação do ambiente virtual com virtualenvwrapper:

::

    $ mkvirtualenv -p /usr/bin/python3 chamados
    $ mkdir -p ~/projetos/python/chamados
    $ cd ~/projetos/python/chamados
    $ setvirtualenvproject

Sempre que precisar ativar o ambiente virtual, por exemplo quando uma nova janela de terminal for aberta.
O virtualenvwrapper tem uma função para ativar o ambiente virtual e mudar para o diretório do projeto, o nome dela é workon:

``$ workon chamados``

Com o ambiente virtual ativado, é possível então instalar as bibliotecas necessárias e realizar as configurações iniciais do Django.

Configurações iniciais do Django
--------------------------------

Ativar o ambiente virtual e então instalar as bibliotecas do projeto, primeiro sem o virtualenvwrapper:

::

    $ cd ~/projetos/python/chamados
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Ou então, se estiver utilizando o virtualenvwrapper:

::

    $ workon chamados
    $ pip install -r requirements.txt

Em seguida o django pode ser configurado.
Configure o seu ambiente, crie um arquivo chamado .env alterando as variáveis necessários:

::

    DEBUG=True
    TEMPLATE_DEBUG=True
    DJANGO_DEBUG=True

    SECRET_KEY_LOCAL=PARADEBUGTANTOFAZ
    SECRET_KEY_PROD=PARADEBUGTANTOFAZ

    DATABASE_URL=sqlite:///db.sqlite
    DATABASE_TEST_URL=sqlite:///db.sqlite

    LDAP_AUTH_URL=ldap://SEU_SERVIDOR_LDAP
    LDAP_AUTH_SEARCH_BASE=ou=Usuarios,dc=XX,dc=COM,dc=BR
    LDAP_AUTH_OBJECT_CLASS=inetOrgPerson

    LDAP_AUTH_USER_FIELDS_USERNAME=CAMPO_USERNAME_ID_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_USERNAME=CAMPO_USERNAME_ID_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_FIRST_NAME=CAMPO_FIRSTNAME_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_LAST_NAME=CAMPO_LASTNAME_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_EMAIL=CAMPO_EMAIL_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_MATRICULA=CAMPO_MATRICULA_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_LOTADO=CAMPO_LOTACAO_DO_SEU_LDAP
    LDAP_AUTH_USER_FIELDS_CHEFIA=CAMPO_CHEFIA_DO_SEU_LDAP

    MSCMC_SERVER=http://SEU_SERVIDOR_DE_SERVICOS.com.br

    EMAIL_HOST='smtp.SEU_SERVIDOR_EMAIL.com.br'
    EMAIL_HOST_USER='USUARIO_QUE_PODE_MANDAR_EMAIL'
    EMAIL_HOST_PASSWORD='SENHA'
    EMAIL_PORT=587
    EMAIL_USE_TLS=True

    CELERY_BROKER_URL='redis+socket:///var/run/redis/redis.sock'

    REDIS_URL='redis+socket:///var/run/redis/redis.sock?virtual_host=0'

Crie as tabelas no banco:

``$ python manage.py migrate``

Instale as dependências do bower:

``$ python manage.py bower_install``

Colete arquivos estáticos:

``$ python manage.py collectstatic``

Rode os testes (alguns testes falham pois o sqlite não valida tamanho de campo, para funcionar utilize o postgresql):

``$ python manage.py test``
