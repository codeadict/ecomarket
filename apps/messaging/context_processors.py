from .models import MessageThread


def inbox(request):
    if request.user.is_authenticated():
        return {
                'new_threads_count': MessageThread.objects.new_threads_count(request.user)}
    else:
        return {}
