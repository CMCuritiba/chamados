# -*- coding: utf-8 -*-

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'chamadoscmc.core'
    verbose_name = "Core"

    def ready(self):
        pass
