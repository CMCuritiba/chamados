# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.
# Copyright (c) The django-ldapdb project

from __future__ import unicode_literals

from ldapdb.models.fields import (CharField, ImageField, ListField, IntegerField)
import ldapdb.models
from django.contrib.auth.models import AbstractUser
from django.db import models

'''
# LDAP User
# -----------------------------------------------------------------------------------------------
class LdapUser(ldapdb.models.Model):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    base_dn = "ou=Usuarios,dc=cmc,dc=pr,dc=gov,dc=br"
    object_classes = ['posixAccount', 'shadowAccount', 'inetOrgPerson']

    # inetOrgPerson
    first_name = CharField(db_column='givenName')
    last_name = CharField(db_column='sn')
    full_name = CharField(db_column='cn')
    email = CharField(db_column='mail')
    #phone = CharField(db_column='telephoneNumber', blank=True)
    #mobile_phone = CharField(db_column='mobile', blank=True)
    #photo = ImageField(db_column='jpegPhoto')

    # posixAccount
    uid = IntegerField(db_column='uidNumber', unique=True)
    group = IntegerField(db_column='gidNumber')
    gecos = CharField(db_column='gecos')
    home_directory = CharField(db_column='homeDirectory')
    login_shell = CharField(db_column='loginShell', default='/bin/bash')
    username = CharField(db_column='uid', primary_key=True)
    password = CharField(db_column='userPassword')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.full_name

# LDAP Group
# -----------------------------------------------------------------------------------------------
class LdapGroup(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = "dc=cmc,dc=pr,dc=gov,dc=br"
    object_classes = ['posixGroup']

    # posixGroup attributes
    gid = IntegerField(db_column='gidNumber', unique=True)
    name = CharField(db_column='cn', max_length=200, primary_key=True)
    usernames = ListField(db_column='memberUid')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
'''
# Usando o AbstractUser para guardar informações extras do LDAP no model
# -----------------------------------------------------------------------------------------------
class User(AbstractUser):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	lotado = models.CharField(max_length=200, blank=True)
	matricula = models.CharField(max_length=200, blank=True)
	chefia = models.NullBooleanField()

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name