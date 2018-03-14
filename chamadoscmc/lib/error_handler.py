# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from .exceptions import BusinessLogicException
from .responses import RedirectToRefererResponse

class HandleBusinessExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, BusinessLogicException):
            message = "Operação Inválida - %s" % exception
            messages.error(request, message)
            return RedirectToRefererResponse(request)