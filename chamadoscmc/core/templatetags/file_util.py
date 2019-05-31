from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def extensao(value):
    arquivo = value.arquivo.path
    extensao = arquivo.split(".")[-1]
    if extensao == 'pdf':
        return mark_safe("""
            {type: "pdf"}
        """)
    else:
        return mark_safe("""
            {}
        """)

