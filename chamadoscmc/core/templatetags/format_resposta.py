from django import template
from django.utils.safestring import mark_safe
from django.template import Context, Template
from django.utils.html import format_html



register = template.Library()

@register.filter(name='format_resposta')
def format_resposta(value):
  return format_html(str(value).replace('\r', "<br/>"))
   