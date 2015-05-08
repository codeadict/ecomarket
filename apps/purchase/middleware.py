# coding=utf-8
from purchase.models import Cart

CART_COOKIE_NAME = 'ecomarket_cart'
CART_COOKIE_MAX_AGE = 60 * 60 * 24 * 30 # 30 days


class AnonymousCart(object):
    """
    This runs *after* authentication middleware.

    If the user is Anonymous they will be assigned a 'cart' object.
    If anything saves that cart (e.g. adding a product), then a cookie will be
    set which allows the Anonymous user to load their cart again in future.

    This makes 'Add to Basket' and first stage of the checkout available to
    all users of the site, regardless of if they're logged in or not.

    After logging in it will check if they had a saved Anonymous cart and
    migrate all the items into the Users cart. This makes the Checkout process
    seamless for anonymous users going through the Login barrier.
    """
    def process_request(self, request):
        # Note: Google Chrome doesn't send cookies on favicon request!!!
        #       this was causing a cart to be created every time the favicon was
        #       hit.
        if request.path == "/favicon.ico":
            return

        # Handle cart migrations after login
        if not request.user.is_anonymous():
            old_cart = None
            old_cart_id = request.get_signed_cookie(CART_COOKIE_NAME, None)
            if old_cart_id:    
                try:
                    old_cart = Cart.objects.get(id=old_cart_id)
                except Cart.DoesNotExist:
                    pass
            # User is logged in, but has an 'anonymous cart cookie'
            if old_cart is not None:
                # If it's been saved, then migrate contents over to User cart
                if old_cart.user is None and old_cart.id is not None and old_cart.id != request.user.cart.id:                    
                    old_cart.move_contents_to(request.user.cart)
                    old_cart.delete()
            request._delete_cart_cookie = True
            return        

        # Load 'Anonymous cart cookie' or create unsaved Cart object
        cart = None
        cart_id = request.get_signed_cookie(CART_COOKIE_NAME, None)
        if cart_id is not None:    
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                pass
        if cart is None:
            cart = Cart()
        request.user.cart = cart
        request._needs_cart_cookie = True

    def process_response(self, request, response):
        if getattr(request, '_delete_cart_cookie', False) is True:
            response.delete_cookie(CART_COOKIE_NAME)
        else:
            needs_cookie = getattr(request, '_needs_cart_cookie', False)
            if getattr(request, 'user', None) is not None:
                if getattr(request.user, 'cart', None) is not None:
                    cart = request.user.cart
                    if needs_cookie and cart.user is None and cart.id is not None:
                        response.set_signed_cookie(CART_COOKIE_NAME, str(request.user.cart.id), max_age=CART_COOKIE_MAX_AGE)
        return response