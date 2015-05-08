from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import Message, MessageThread, ThreadUserState
from .fields import CommaSeparatedUserInput, CommaSeparatedUserField


class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"),
                    widget=CommaSeparatedUserInput(
                            attrs={
                                'placeholder': _(u"User (Start typing and we'll help you!)"),
                                'data-source-url': '/messages/inbox/compose/recipient-list/',
                            })
                    )
    subject = forms.CharField(label=_(u"Subject"),
                    widget=forms.TextInput(
                            attrs={'maxlength': 120, 'placeholder': "Subject"})
                    )
    body = forms.CharField(label=_(u"Body"),
                    widget=forms.Textarea(
                        attrs={'placeholder': 'Message'})
                    )

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter:
            self.fields['recipient']._recipient_filter = recipient_filter

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        # Validating that logged in user can reply to only one recipient.
        if len(recipients) > 1:
            raise forms.ValidationError(_(u"You can only send a message to one user."))
        else:
            subject = self.cleaned_data['subject']
            body = self.cleaned_data['body']
            recipient = recipients[0]
            msg = Message(
                sender=sender,
                recipient=recipient,
                subject=subject,
                body=body,
            )
            now = timezone.now()

            if parent_msg:
                msg.thread = parent_msg.thread
                try:
                    thread_sender_state = ThreadUserState.objects.get(thread=msg.thread, user=sender)
                    thread_sender_state.read_at = now
                    thread_sender_state.save()
                except ThreadUserState.DoesNotExist:
                    pass

                try:
                    # If reciepient has deleted this thread we should pass it as non deleted
                    thread_recipient_state = ThreadUserState.objects.get(thread=msg.thread, user=recipient)
                    if thread_recipient_state.deleted_at:
                        thread_recipient_state.deleted_at = None
                    thread_recipient_state.read_at = None
                    thread_recipient_state.save()
                except ThreadUserState.DoesNotExist:
                    ThreadUserState.objects.create(thread=msg.thread, user=recipient)

                msg.parent_msg = parent_msg
                parent_msg.replied_at = now
                parent_msg.read_at = now
                parent_msg.save()
            else:
                # New message; no previous thread history.
                thread = MessageThread.objects.create()
                msg.thread = thread
                ThreadUserState.objects.create(thread=thread, user=recipient)

                thread_sender_state = ThreadUserState.objects.create(thread=thread, user=sender)
                thread_sender_state.read_at = now
                thread_sender_state.save()
            msg.save()
            return msg
