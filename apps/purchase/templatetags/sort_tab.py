from django.template.loader import get_template

def sort_tab(parser, token):
    try:
        tag_name, fieldname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument"
                                           " which is the fieldname to sort".
                                           format(token.contents.split()[0]))
