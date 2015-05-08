"""
Help and Examples
=================

If you need to enclose your arguments in quotes the please do so, if you don't,
then don't. They will be stripped out where necessary.

Top of page
-----------

Alert types:
 * info
 * success
 * warning
 * error
 * answer

{% alert error "Oh noes!" "You forgot to include your socks." %}
{% alert info "Let me help you" "You need to buy some new socks." http://lmgtfy.com?q=eco+socks %}


Lightbox
--------

This takes 3 required arguments:
 * element id (you'll need to use this in your link that pops up the lightbox)
 * heading
 * body

There are 3 optional arguments:
 * do action (adds a primary action button with this variable as the button text)
 * help link (adds help button that opens new tab with this url)
 * image url (should be 180px in width)

To leave an optional argument out you can use the empty string ('') unless
it's at the end of the list in which case just omit it.

Getting the modal HTML out
..........................

Example with required arguments only:
```
{% lightbox my_modal_id 'Hi!' '<p>Bacon Ipsum la di da.</p>' %}
```

Example with image but not help link or action button:
```
{% lightbox my_modal_id 'Hi!' '<p>Bacon Ipsum la di da.</p>'  '' 'http://stage.ecomarket.com/static/tmp/blog/265x200/1.jpg' %}
```

Activating the modal
....................

The above will give you a hidden modal in your DOM. You need a way of
activating it.

<a href="javascript:void(0)" class="btn btn-flat btn-blue modal" data-toggle="modal" data-target="#my_modal_id">Greet Me</a>

Make sure the data-target is the same id you gave to the template tag.

Adding action buttons
.....................

Things get a bit more complicated now.

```
{% lightbox my_modal_id 'Hi!' '<p>Bacon Ipsum la di da.</p>' '' '' 'Alert me' 'my_button_id' %}
```

That will give you a lightbox as before but with the addition of a primary
action button with the ID specified. You need to use the ID to hook into the
button click. You also need to take care of closing the modal yourself when
the custom button is clicked.

```
<script type="text/javascript">
    $('#my_button_id').on('click', function() {
        alert('You clicked the action button!');
        $("#my_modal_id").modal("hide");
    });
</script>
```

You will still need the button to activate the modal too (see above).
"""

from django import template
from django.template.loader import render_to_string


register = template.Library()


def unpack_string(value):
    """
    Sometimes (often) you'll need to pass quoted strings to these tags. This
    function will strip out the beginning and ending quotes allowing you to
    use the empty string ('') for optional arguments.
    """
    if not value or len(value) < 2:
        return value
    if value[0] == value[-1] and value[0] in ['"', "'"]:
        return value[1:-1]
    return value


# Top-of-page alerts

@register.tag(name="alert")
def alert(parser, token):
    try:
        tag_name, alert_type, heading, body = token.split_contents()
        help_link = None
    except ValueError:
        try:
            tag_name, alert_type, heading, body, help_link = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                "%r tag requires 3 or 4 arguments (alert type, heading, body, [help link])"
                % token.contents.split()[0])

    return AlertNode(
        unpack_string(alert_type),
        unpack_string(heading),
        unpack_string(body),
        unpack_string(help_link)
    )


class AlertNode(template.Node):
    def __init__(self, alert_type, heading, body, help_link=None):
        self.alert_type = alert_type
        self.heading = heading
        self.body = body
        self.help_link = help_link

    def render(self, context):
        template = 'alerts/top.html'
        return render_to_string(
            template, {
                'alert_type': self.alert_type,
                'heading': self.heading,
                'body': self.body,
                'help_link': self.help_link,
            }
        )


## Pre-defined alerts

@register.tag(name="alert_invalid_form")
def alert_invalid_form(parser, token):
    parts = token.split_contents()
    if len(parts) > 1:
        raise template.TemplateSyntaxError("%r tag has no arguments" % parts[0])

    return AlertNode('error', 'Oops! Looks like something was incorrect',
        'Please check over the details your entered below and correct any errors. Thanks!'
    )


# Lightbox alerts

@register.tag(name="lightbox")
def lightbox(parser, token):
    # Required: element_id, heading, body
    # Optional: do_action, help_link, image_src

    parts = token.split_contents()
    parts_len = len(parts)

    if parts_len not in [4, 5, 6, 8]:
        raise template.TemplateSyntaxError(
            "%r tag requires 3, 4, 5 or 7 arguments (element_id, heading, body, [help_link, image_src, button_text, button_id])"
            % parts[0])

    element_id, heading, body = parts[1:4]
    help_link = image_src = button_text = button_id = None

    if parts_len >= 5:
        help_link = parts[4]
    if parts_len >= 6:
        image_src = parts[5]
    if parts_len > 7:
        button_text = parts[6]
        button_id = parts[7]

    return LightboxNode(
        unpack_string(element_id),
        unpack_string(heading),
        unpack_string(body),
        unpack_string(help_link),
        unpack_string(image_src),
        unpack_string(button_text),
        unpack_string(button_id),
    )


class LightboxNode(template.Node):
    def __init__(self, element_id, heading, body, help_link, image_src, button_text, button_id):
        # Required
        self.element_id = element_id
        self.heading = heading
        self.body = body
        # Optional
        self.help_link = help_link
        self.image_src = image_src
        self.button_text = button_text
        self.button_id = button_id

    def render(self, context):
        template = 'alerts/lightbox.html'
        return render_to_string(
            template, {
                'element_id': self.element_id,
                'heading': self.heading,
                'body': self.body,
                'help_link': self.help_link,
                'image_src': self.image_src,
                'button_text': self.button_text,
                'button_id': self.button_id,
            }
        )
