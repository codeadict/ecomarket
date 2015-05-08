import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import (ListView,
                                  TemplateView,
                                  DetailView)
from django.utils.decorators import method_decorator

from main.utils.http import JsonResponse

from notifications import Events

from .models import Message, MessageThread, ThreadUserState
from .forms import ComposeForm
from .utils import (format_quote,
                    mark_action_thread,
                    message_to_reply)
from marketplace.models import Product, Country


class BaseMessagingListView(ListView):
    context_object_name = "thread_list"

    def get_queryset(self):
        # For now the outbox is disabled so we can restrict all views to
        # inbox threads.
        return MessageThread.objects.all_threads_for(self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseMessagingListView, self).dispatch(*args, **kwargs)

    def get_paginate_by(self, *args, **kwargs):
        paginate_by = super(BaseMessagingListView, self).get_paginate_by(*args, **kwargs)
        try:
            paginate_by = self.request.GET['page-count']
            paginate_by = int(paginate_by) if paginate_by != 'all' else 1000
        except KeyError:
            paginate_by = 12

        return paginate_by


class InboxView(BaseMessagingListView):
    template_name = "messaging/inbox_outbox.html"

    def get_queryset(self):
        return MessageThread.objects.all_threads_for(self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InboxView, self).get_context_data(**kwargs)
        # Add in the tab
        context['tab'] = 'inbox'
        return context


class OutboxView(BaseMessagingListView):
    template_name = "messaging/inbox_outbox.html"

    def get_queryset(self):
        return MessageThread.objects.outbox_threads_for(self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(OutboxView, self).get_context_data(**kwargs)
        # Add in the tab
        context['tab'] = 'outbox'
        return context


@login_required
def trash(request, template_name='django_messages/trash.html'):
    """
    Displays a list of deleted messages.
    Optional arguments:
        ``template_name``: name of the template to use
    Hint: A Cron-Job could periodicly clean up old messages, which are deleted
    by sender and recipient.
    """
    message_list = Message.objects.trash_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))


@login_required
def compose(request, recipient=None, form_class=ComposeForm,
            success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if not recipient_filter:
        recipient_filter = [request.user]
    form = form_class(request.POST or None, recipient_filter=recipient_filter)
    recipients = []
    if request.method == "POST":
        if form.is_valid():
            message = form.save(sender=request.user)
            Events(request).message_sent(message)
            if request.GET.get('product_to_be_delivered', None):
                country = Country.objects.get(code=request.country)
                product = Product.objects.get(pk=request.GET.get('product_to_be_delivered', None))

                index = 1
                cats = product.category_objs()
                i = 0
                related_search_category = None
                for v in cats:
                    if i == index:
                        related_search_category = v
                    i = i + 1

                messages.success(request, _(u"Your message has been sent. Great job! \
                    In the mean time why don't you <a href=\"{url}\">check out these products</a> that do \
                    deliver to {country}".format(
                        country=country.title,
                        url=reverse('category_discover', args=(related_search_category.slug,))
                    )))
            else:
                messages.success(request, _(u"Your message has been sent. Great job!"))

            if not request.is_ajax():
                success_url = request.GET.get('next', '') or \
                                reverse('messaging_inbox')
                return HttpResponseRedirect(success_url)
    else:
        if recipient is not None:
            # Todo: recipient can be email address too?
            recipients = [u for u in User.objects.filter(username__in=[r.strip() for r in recipient.split('+')])]
            if len(recipients) > 1:
                form.recipient.error_messages['recipient_error'] = "You must send a message to only one user."
            form.fields['recipient'].initial = recipients
        if request.GET.get('request_delivery_to_country', None):
            country = Country.objects.get(code=request.country)
            product = Product.objects.get(pk=request.GET.get('product_to_be_delivered', None))
            form.fields['subject'].initial = 'I would like to buy your product delivered to %s' % country.title
            form.fields['body'].initial = '''Hello {stall_owner},

I am trying to buy a {product}... however you don't have shipping rates set up for {country}.

Could you please let me know if this is possible and update your \
shipping rates to include {country} if so, on Eco Market, so that \
I can purchase the above. \
You can see how to do this in the help center at \
http://help.ecomarket.com/customer/portal/articles/398297-how-to-create-and-apply-shipping-rates

{customer}'''.format(
        stall_owner=str(product.stall.user).capitalize(),
        country=country.title,
        product=str(product.title).lower(),
        customer=str(request.user.first_name).capitalize()
    )

    if request.is_ajax():
        product = None
        if request.GET.get('request_delivery_to_country', None):
            product = Product.objects.get(pk=request.GET.get('product_to_be_delivered', None))
        template_name = 'messaging/fragments/_modal_compose_form.html'
        if product:
            return render_to_response(template_name, {
                'form': form,
                'product_to_be_delivered': product.id,
            }, context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, {
                'form': form,
            }, context_instance=RequestContext(request))

    template_name = 'messaging/compose.html'
    _recipient = None
    if recipient and recipients:
        _recipient = recipients[0].username
    return render_to_response(template_name, {
        'form': form,
        'recipient': _recipient
    }, context_instance=RequestContext(request))


@login_required
def reply(request, message_id, form_class=ComposeForm,
        template_name='messaging/fragments/_modal_reply_form.html', success_url=None,
        recipient_filter=None, quote_helper=format_quote):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)
    user = request.user
    if parent.sender != user and parent.recipient != user:
        raise Http404

    if request.method == "POST":
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            msg = form.save(sender=user, parent_msg=parent)
            Events(request).message_sent(msg)            

            if request.GET.get('resolve') == '1':
                mark_action_thread(user, parent.thread, 'resolved')

            messages.success(request, _(u"Your message has been sent. Great job!"))
            if not request.is_ajax():
                if success_url is None:
                    success_url = reverse('messaging_inbox')
                    return HttpResponseRedirect(success_url)
    else:
        thread = parent.thread
        thread_user_state = ThreadUserState.objects.get(thread=thread, user=user)
        thread_user_state.read_at = datetime.datetime.now()
        thread_user_state.save()

        recipient = parent.sender
        if recipient == user:
            # Find the real recipient.
            recipient = thread.messages.exclude(recipient=user)[0].recipient

        form = form_class(initial={
            'body': quote_helper(parent.sender, parent.body),
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'recipient': [recipient]
            })

    return render_to_response(template_name, {
        'form': form,
        'message_id': message_id,
        'subject': parent.subject,
        'message_list': parent.thread.messages.all().order_by('sent_at'),
        'message_to_reply': message_to_reply(parent.thread, user)
    }, context_instance=RequestContext(request))


@login_required
def delete(request, message_id, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely.
    A cron-job should prune the database and remove old messages which are
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False

    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']

    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True

    if deleted:
        message.save()
        messages.info(request, _(u"Your message(s) have been deleted and recycled!"))
        return HttpResponseRedirect(success_url)

    raise Http404


@login_required
def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if 'next' in request.GET:
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        messages.info(request, _(u"Message successfully recovered."))
        return HttpResponseRedirect(success_url)
    raise Http404


# Ajax

class UserNewMessagesCount(TemplateView):
    template_name = 'fragments/_new_messages_count.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserNewMessagesCount, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserNewMessagesCount, self).get_context_data(**kwargs)
        context['new_threads_count'] = MessageThread.objects.new_threads_count(self.request.user)
        return context


class ViewThread(DetailView):
    queryset = MessageThread.objects.all()
    template_name = 'messaging/view_thread_messages.html'
    context_object_name = "thread"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        now = datetime.datetime.now()
        context = super(ViewThread, self).get_context_data(**kwargs)
        user = self.request.user
        thread = context['thread']
        tab = self.kwargs['tab']
        context['tab'] = tab
        thread_user_state = ThreadUserState.objects.get(thread=thread, user=user)
        thread_user_state.read_at = now
        thread_user_state.save()
        context['message_to_reply'] = message_to_reply(thread, user)
        context['from'] = "view"
        return context


class MultipleMessageSelectedView(BaseMessagingListView):
    model = MessageThread
    context_object_name = ""
    template_name = 'messaging/fragments/_messages_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MultipleMessageSelectedView, self).get_context_data(**kwargs)

        tab = 'inbox'
        if 'all' in self.request.GET:
            str_list = dict(self.request.GET)['all']
            thread_id_list = [int(unicode_id) for unicode_id in str_list]
        else:
            raise Http404
        if 'tab' in self.request.GET:
            tab = str(self.request.GET['tab'])
        else:
            raise Http404

        # Adding "tab" to context
        context['tab'] = tab

        messaging_threads = MessageThread.objects.filter(pk__in=thread_id_list)

        # Adding "thread_qs" to context
        context['thread_qs'] = messaging_threads

        return context


class MarkSelectedView(MultipleMessageSelectedView):

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MarkSelectedView, self).get_context_data(**kwargs)

        # Getting the "action" to do, it is passed through url as a kwargs param,
        # "action" can be "read"|"unread"|"resolved"|"unresolved"|"delete".
        action = self.kwargs['mark']

        # Getting "tab" which can take the value inbox/outbox
        tab = context['tab']

        user = self.request.user
        thread_qs = context['thread_qs']
        for thread in thread_qs:
            marked = mark_action_thread(user, thread, action, tab)
            if not marked:
                raise Http404

        suppress_messages = self.request.GET.get('suppress_messages') == '1'
        if not suppress_messages:
            if action == 'delete':
                message = _(u"Your message%s been deleted and recycled!" % ('s have' if len(thread_qs) > 1 else ' has',))
            elif action == 'unread':
                message = _(u"We have marked %s as being unread again." % ('these messages' if len(thread_qs) > 1 else 'this message',))
            else:
                message = _(u"We have marked %s as being %s." % ('these messages' if len(thread_qs) > 1 else 'this message', action,))
            messages.success(self.request, message)

            #if notification:
                #notification.send([user], "messages_deleted", {'message': message,})

        # Deleting "thread_qs" from context,
        # because this list isn't usefull already.
        del context['thread_qs']

        thread_list = MessageThread.objects.all_threads_for(user)

        # Adding "thread_list" to context
        context['thread_list'] = thread_list

        return context


class PlainMessageList(BaseMessagingListView):

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlainMessageList, self).get_context_data(**kwargs)
        user = self.request.user
        thread_list = MessageThread.objects.all_threads_for(user)

        # Adding "thread_list" to context
        context['thread_list'] = thread_list

        return context


def recipient_typeahead(request):
    query = request.GET.get('query')
    users = User.objects.exclude(pk=request.user.pk)
    if query:
        users = users.filter(username__icontains=query)
    users = users.order_by('username')[:12]
    usernames = [user.username for user in users]
    return JsonResponse(data={'recipients': usernames})
