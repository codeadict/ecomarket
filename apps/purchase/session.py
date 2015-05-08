import logging

from purchase.models import Cart

logger = logging.getLogger(__name__)


CART_ID = 'CART-ID'


class CartSession(object):
    """
    This is a wrapper around the users session to automatically
    fetch/create a current Cart instance and interact with it.

    You can directly interact with the returned Cart instance to add/remove
    products. This class is only used to fetch it from session.

    """

    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            logger.debug("Retreived saved Cart(id={0}) from session".format(
                cart_id))
            try:
                # do we need a separate flag for total cart checked_out?
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = self.new(request)
        else:
            logger.debug("No existing Cart found, creating a new one.")
            cart = self.new(request)
        self.cart = cart

    def new(self, request):
        """Creates a new Cart and saves id to users session."""
        cart = Cart(user=request.user)
        cart.save()
        logger.debug("Created new Cart(id={0})".format(cart.id))
        request.session[CART_ID] = cart.id
        logger.debug("Saving Cart(id={0}) to session".format(cart.id))
        return cart

    def remove(self, request):
        """Removes saved Cart id from users session."""
        if CART_ID in request.session:
            del(request.session[CART_ID])

    def get(self):
        return self.cart
