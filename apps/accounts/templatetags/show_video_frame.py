# -*- encoding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('accounts/video/fragments/video_frame.html', takes_context=True)
def show_video_frame(context, video, width=400, height=300):
    """
    Render a video iFrame

    usage example:

       {% show_video_frame video %}

    :param context: added automatically by django
    :param width: width of the iframe
    :param height: height of the iframe
    :return:
    """
    context["video"] = video
    context['width'] = width
    context['height'] = height
    return context