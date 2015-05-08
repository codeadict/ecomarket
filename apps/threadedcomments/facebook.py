import requests

from django.conf import settings

from rollyourown.seo import get_metadata


if settings.DEBUG:
    ACCESS_TOKEN = getattr(settings, "FACEBOOK_TESTING_ACCESS_TOKEN", None)
else:
    ACCESS_TOKEN = None


class FacebookErrorMessage(requests.exceptions.HTTPError):
    pass


def post_comment_to_facebook(request, user, comment):
    # TODO factor this stuff out into an opengraph/facebook app
    social_auth = user.social_auth.get(provider="facebook")
    url = "https://graph.facebook.com/me/{ns}:comment_on".format(
        ns=settings.FACEBOOK_NAMESPACE,
    )
    object_url = comment.content_object.get_absolute_url()
    object_type = get_metadata(object_url).og_type.value
    if object_type is None:
        raise AttributeError("Unable to find og:type from URL %s" % object_url)
    # Remove namespace, if any
    if ":" in object_type:
        unused, object_type = object_type.split(":", 1)
    data = {
        "access_token": ACCESS_TOKEN or social_auth.extra_data["access_token"],
        object_type: "http://{host}{path}".format(
            host=request.get_host(),
            path=object_url,
        ),
        "fb:explicitly_shared": True,
        "message": comment.comment,
    }
    resp = requests.post(url, data)
    resp_data = resp.json
    if resp.status_code != requests.codes.ok:
        e = FacebookErrorMessage("%s: %s" % (
            resp_data["error"]["type"], resp_data["error"]["message"]))
        e.response = resp
        raise e
    if "id" in resp_data:
        return resp_data["id"]
    raise requests.exceptions.HTTPError("Unknown data: %s" % resp_data)
