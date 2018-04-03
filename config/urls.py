# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from autentica.util.mixin import CMCLoginRequired
from chamadoscmc.core.views import MyIndexView
from chamadoscmc.core.views import AcessoAdmin


urlpatterns = [
    url(r'^autentica/', include('autentica.urls', namespace='autentica')),
    url(r'^$', MyIndexView.as_view(), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^fila/', include('chamadoscmc.core.urlsfila', namespace='fila')),
    url(r'^chamado/', include('chamadoscmc.core.urls', namespace='chamado')),
    url(r'^cadastro/', include('chamadoscmc.core.cadastro_urls', namespace='cadastro')),
    url(r'^relatorio/', include('chamadoscmc.core.relatorio_urls', namespace='relatorio')),
    url(r'^acesso/admin/$', AcessoAdmin.as_view(), name='acesso-admin'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),


] 

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ] 

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]


