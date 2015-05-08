"""
Tag for creating social buttons with correct metadata
from template variables.

Uses Sharrre (http://sharrre.com/).

don't for get to add the html!!!
<div class="social"><div id="shareme"></div></div>
"""
from django import template

from apps.marketplace.models import Stall, Product
from apps.lovelists.models import LoveList
from apps.articles.models import Article
from main.utils import absolute_uri
import settings

import json
from itertools import chain
from random import sample
from copy import deepcopy

register = template.Library()


class ShareNode(template.Node):
    SHARRRE_LIB_PATH = settings.STATIC_URL + 'js/vendor/jquery.sharrre-1.3.2.min.js'
    SHARRRE_SCRIPT = '<script type="text/javascript" src="%s"></script>' % SHARRRE_LIB_PATH
    SCRIPT = '''
    <script type="text/javascript">
    $(function() {
      $('#').sharrre(%s);
    });
    </script>

    '''
    DEFAULT_MEDIA = settings.STATIC_URL + 'images/ecomarket.png'
    DEFAULT_OPTIONS = {
        'share': {
            'twitter': True,
            'facebook': True,
            'googlePlus': True,
            'pinterest': True,
        },
        'enableHover': False,
        'enableCounter': False,
        'enableTracking': True,
        'className': 'sharrre vertical',
        'url': 'http://www.ecomarket.com',
        'buttons': {
            'googlePlus': {
                'size':'medium',
                'annotation':'none',
            },
            'facebook': {
                'layout':'button_count',
                'faces':False,
            },
            'twitter': {
                'via':'ecomarket',
            },
            'pinterest': {
                'media': absolute_uri(DEFAULT_MEDIA),
            }
        }
    }

    def __init__(self, incl_script, obj=None, style='vertical', ele_id='#shareme'):
        self.incl_script = incl_script
        if obj is not None:
            self.obj = template.Variable(obj)
        else:
            self.obj = obj
        self.style = style
        self.ele_id = ele_id

    def render(self, context):
        script = self.SCRIPT
        script = script.replace('#', self.ele_id)
        options = self.get_defaults()

        if self.incl_script:
            script = self.SHARRRE_SCRIPT + script

        if self.obj is None:
            # like facebook page if there is no content to share
            options['buttons']['facebook']['url'] = 'http://www.facebook.com/ecomarketdotcom'
            return script % json.dumps(options)
        else:
            try:
                obj = self.obj.resolve(context)
            except template.VariableDoesNotExist:
                raise template.TemplateSyntaxError(
                        'could not resolve %s' % self.obj
                        )

            if type(obj) not in [Article, Product, Stall, LoveList]:
                raise template.TemplateSyntaxError(
                        'social_script tag requires an object of type Article,' \
                        + ' Product, Stall or LoveList as the first argument ' \
                        + 'recieved type %s' % type(obj)
                        )

            if self.style == 'horizonal':
                options['className'] = 'sharrre horizontal'

            tags = []

            # Stall
            if type(obj) == Stall:
                text = 'Loving %s on Eco Market' % obj.title
                media = absolute_uri(obj.user.get_profile().avatar_228)
                if media is None:
                    media = self.DEFAULT_MEDIA
            # Product
            elif type(obj) == Product:
                text = 'Loving this %s on Eco Market' % obj.title
                media = obj.image.url_400
                tags = obj.causes.all()[:3]
                tags = list(chain(tags, obj.keywords.all()[:2]))
            # Article
            elif type(obj) == Article:
                text = obj.title
                tags = obj.tags.all()[:3]
                if obj.youtube_video is not None:
                    media = obj.youtube_video['url']
                elif obj.attachments.exists():
                    attachment = obj.attachments.latest('id')
                    media = absolute_uri(attachment.attachment.url)
                else:
                    media = self.DEFAULT_MEDIA
            # LoveList
            elif type(obj) == LoveList:
                text = 'Loving %s by %s on Eco Market' % (obj.title, obj.user.get_name())
                tags.append(str(obj.primary_category))
                tags.append(str(obj.secondary_category))
                media = absolute_uri(obj.products.latest('id').image.url_80)

            # sharing options..
            options['text'] = text
            options['url'] = absolute_uri(obj.get_absolute_url())
            options['buttons']['twitter']['hashtags'] = ','.join([str(t) for t in tags]),
            options['buttons']['pinterest']['media'] = media
            options['buttons']['pinterest']['description'] = text
            return script % json.dumps(options)

    def get_defaults(self):
        ''' storing options in nestled dictionaries is a bad idea.'''
        return deepcopy(self.DEFAULT_OPTIONS)



def share(parser, token, incl_script=False):
    template, line = token.source
    try:
        tag, obj, style, ele_id = token.split_contents()
        return ShareNode(incl_script, obj, style, ele_id)
    except ValueError:
        try:
            tag, arg1, arg2 = token.split_contents()
            if arg1 in ('horizontal','vertical'):
                assert arg2.startswith('#')
                return ShareNode(incl_script, style=arg1, ele_id=arg2)
            else:
                if arg2 in ('horizontal', 'vertical'):
                    return ShareNode(incl_script, obj=arg1, style=arg2)
                else:
                    assert arg2.startswith('#')
                    return ShareNode(incl_script, obj=arg1, ele_id=arg2)
        except ValueError:
            try:
                tag, arg1 = token.split_contents()
                if arg1 in ('horizontal','vertical'):
                    return ShareNode(incl_script, style=arg1)
                elif arg1.startswith('#'):
                    return ShareNode(incl_script, ele_id=arg1)
                else:
                    return ShareNode(incl_script, obj=arg1)
            except ValueError:
                try:
                    tag = token.split_contents()
                    return ShareNode(incl_script)
                except ValueError:
                    raise template.TemplateSyntaxError(
                        '%s tag requires 0,1,2 or 3 args, in order. arg1(optional) = object to share.'
                        + ' arg2(optional) = style (horizontal or vertical).'
                        + ' arg3(optional) = element id to use (must start with #)'
                        % token.contents.split()[0]
                        )

def share_script(parser, token):
    return share(parser, token, incl_script=True)

register.tag(share_script)
register.tag(share)
