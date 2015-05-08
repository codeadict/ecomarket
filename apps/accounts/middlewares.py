
class SailthruLoginCookie(object):
    def process_response(self, request, response):
        sailthru_hid = getattr(request, 'set_sailthru_hid', None)
        if sailthru_hid and 'sailthru_hid' not in request.COOKIES:
            # We are setting a hard value to the domain here since we need to the cookie to be cross-domain
            # Refer to card #678 on Trello.
            response.set_cookie('sailthru_hid', sailthru_hid, max_age=365*24*60*60, domain=".ecomarket.com")
        return response