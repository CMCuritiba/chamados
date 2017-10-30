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

postgres:///chamados-testContribuindo
------------

Crie um fork e clone o repositório:

```
$ git clone https://github.com/SEU_USUARIO_GITHUB/chamados
```

Adicione o repositório remoto upstream:

```
$ git remote add upstream git@github.com:CMCuritiba/chamados.git
```

Configure o seu ambiente, crie um arquivo chamado .env alterando as variáveis necessários:

```
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
```

Crie as tabelas no banco:

```
$ python manage.py migrate
```

Instale as dependências do bower:

```
$ python manage.py bower_install
```

Colete arquivos estáticos:

```
$ python manage.py collectstatic
```

Rode os testes (alguns testes falham pois o sqlite não valida tamanho de campo, para funcionar utilize o postgresql):

```
$ python manage.py test
```
