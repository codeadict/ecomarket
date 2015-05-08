from django.http import Http404
from django.contrib.auth.decorators import user_passes_test

def _has_seller_account(user):
    if not user.is_authenticated():
        # send to login page
        return False
    elif not user.get_profile().is_seller:
        # This seems a bit hacky, but the problem here is that returning False
        # automatically sends us to the login page (not what we want)
        raise Http404("This page does not exist for this user")
    return True

seller_account_required = user_passes_test(_has_seller_account)


def _is_video_beta_stall(user):
    if not user.is_authenticated():
        # send to login page
        return False
    elif not user.get_profile().is_seller:
        # This seems a bit hacky, but the problem here is that returning False
        # automatically sends us to the login page (not what we want)
        raise Http404("This page does not exist for this user")
    elif not user.stall.is_in_video_beta:
        raise Http404("This page does not exist for this user")
    return True

seller_video_beta_required = user_passes_test(_is_video_beta_stall)
