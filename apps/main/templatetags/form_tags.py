from django.template import Library

register = Library()


@register.inclusion_tag("fragments/form_field_snippet.html")
def form_field(field):
    return {"field": field}
