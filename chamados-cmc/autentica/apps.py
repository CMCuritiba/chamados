# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class AutenticaConfig(AppConfig):
    name = 'chamados-cmc.autentica'
    verbose_name = "Autenticação"

    def ready(self):
        pass
