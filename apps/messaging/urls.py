from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from .views import (InboxView,
                    OutboxView,
                    MarkSelectedView,
                    UserNewMessagesCount,
                    ViewThread,
                    PlainMessageList)


urlpatterns = patterns('messaging.views',
    url(r'^inbox/$', InboxView.as_view(), name="messaging_inbox"),
    url(r'^$', redirect_to, {'url': 'inbox/'}, name='messaging_redirect'),
    url(r'^compose/$', 'compose', name='messaging_compose'),
    url(r'^compose/(?P<recipient>[a-zA-Z0-9 @_\.,+!?-]+)/$', 'compose', name='messaging_compose_to'),
    url(r'^inbox|outbox/compose/recipient-list/$', 'recipient_typeahead', name='messaging_compose_recipient_list'),
    url(r'^reply/(?P<message_id>[\d]+)/$', 'reply', name='messaging_reply'),
    url(r'^(?P<tab>[\w.]+)/(?P<pk>[\d]+)/$', ViewThread.as_view(), name='view_thread'),
    url(r'^delete/selected/$', MarkSelectedView.as_view(), {'mark': 'delete'}, name='messaging_delete_selected'),
    url(r'^mark/selected/$', MarkSelectedView.as_view(), {'mark': 'read'}, name='messaging_mark_read_selected'),
    url(r'^markunread/selected/$', MarkSelectedView.as_view(), {'mark': 'unread'}, name='messaging_mark_unread_selected'),
    url(r'^markresolved/selected/$', MarkSelectedView.as_view(), {'mark': 'resolved'}, name='messaging_mark_resolved_selected'),
    url(r'^markunresolved/selected/$', MarkSelectedView.as_view(), {'mark': 'unresolved'}, name='messaging_mark_unresolved_selected'),
    url(r'^list/$', PlainMessageList.as_view(), name='messaging_plain_list'),
    url(r'^user/new/messages/$', UserNewMessagesCount.as_view(), name='messaging_new_messages_count'),
    # url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messaging_delete'),
    # url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messaging_undelete'),
    # url(r'^trash/$', trash, name='messaging_trash'),
)
