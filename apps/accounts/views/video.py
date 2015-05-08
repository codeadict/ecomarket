# coding=utf-8
import datetime
from annoying.decorators import ajax_request
from django.contrib import messages
from django.template import Context, loader
from djipchat.lib import send_to_hipchat
import simplejson as json
from django.views.generic import View, ListView, TemplateView, DetailView

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from apps.accounts.models import Video, VideoType
from main.utils.decorators import view_dispatch_decorator
from accounts.utils import seller_account_required, seller_video_beta_required


@view_dispatch_decorator(seller_video_beta_required)
class VideoAdminView(ListView):
    template_name = 'accounts/video/admin.html'
    model = Video

    class Action:
        DELETE = 'delete'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super(VideoAdminView, self).get_context_data(**kwargs)

        context.update({
            'Action': self.Action,
        })
        return context

    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids')
        action = request.POST.get('action')
        if ids and action == self.Action.DELETE:
            self.get_queryset().filter(pk__in=ids).delete()

        return HttpResponseRedirect(
            reverse('video')
        )


@view_dispatch_decorator(seller_video_beta_required)
class VideoCreateView(TemplateView):
    template_name = 'accounts/video/create.html'

    def get_context_data(self, **kwargs):
        context = super(VideoCreateView, self).get_context_data(**kwargs)
        context['video_type'] = VideoType.objects.get(pk=1)
        return context

    @ajax_request
    def post(self, *args, **kwargs):
        vid_type = VideoType.objects.get(pk=1)
        vid = Video(
            video_guid=self.request.POST['guid'],
            embed_url=self.request.POST['embed_url'],
            splash_url=self.request.POST['splash_url'],
            user=self.request.user,
            video_type=vid_type
        )
        vid.save()

        messages.info(
            self.request,
            'Great job! Your video has been saved. Since we are still testing this feature we will manually review videos and get back to you about these shortly'
        )

        # send notification to hipchat
        template_context = Context({
            'request': self.request,
            'user': self.request.user,
            'now': datetime.datetime.now()
        })
        template = loader.get_template("accounts/video/fragments/hipchat_notification.html")
        output = template.render(template_context)

        send_to_hipchat(
            output,
            room_id=82667,
            notify=1,
        )

        return {
            "success": True
        }


@view_dispatch_decorator(seller_video_beta_required)
class VideoEditView(DetailView):
    template_name = 'accounts/video/edit.html'
    model = Video
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super(VideoEditView, self).get_context_data(**kwargs)
        video = self.get_object()
        context['video'] = video
        return context

    @ajax_request
    def post(self, request, *args, **kwargs):
        video = self.get_object()

        if video.user != request.user:
            raise Exception("Error!!! Wrong user")

        video.video_guid = self.request.POST['guid']
        video.embed_url = self.request.POST['embed_url']
        video.splash_url = self.request.POST['splash_url']
        video.save()

        messages.info(
            request,
            'Done, your video has now been edited. We are manually processing these at the moment whilst this feature is quite new so we will get back to you shortly after reviewing this.',
        )

        return {
            "success": True
        }
