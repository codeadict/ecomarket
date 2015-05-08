import django.template

register = django.template.Library()


@register.inclusion_tag("lovelists/fragments/love_this_button.html")
def love_this_button(user, product):
    if user.is_authenticated():
        loved = (product.love_lists.filter(user=user).count() > 0)
    else:
        loved = False
    return {
        "loved": loved,
        "product": product,
    }
