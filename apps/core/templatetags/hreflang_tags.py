from django import template
from django.urls.base import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def hreflang_url(context, lang_code):
    request = context.get("request")
    if not request:
        return ""
    return translate_url(request.path, lang_code)
