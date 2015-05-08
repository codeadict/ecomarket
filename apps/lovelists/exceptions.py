class TooManyOwnProductsLoved(Exception):

    error_dialog_text = {
        "title": "Sorry, you have to share the love a bit more!",
        "description": (
            "It seems you have tried to love more than 50 percent of your own "
            "items in this list. Whilst love lists are a great way to promote "
            "products, they are much better for everyone if they contain a "
            "mix of products, so in order to add more of your own please "
            "ensure you balance this out with other stall owners' products at "
            "least half and half."
        ),
        "dismiss": "OK, roger that!",
    }

    def __init__(self, limit):
        super(TooManyOwnProductsLoved, self).__init__(
            "Current limit is %d" % limit)
        self.limit = limit
