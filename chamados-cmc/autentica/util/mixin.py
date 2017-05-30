# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from braces import views

class CMCAdminLoginRequired(views.LoginRequiredMixin, views.SuperuserRequiredMixin):
	login_url = "/autentica/loga/"

class CMCLoginRequired(views.LoginRequiredMixin):
	login_url = "/autentica/loga/"