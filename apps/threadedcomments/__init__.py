from .forms import CommentFormWithSpamish
from .models import ThreadedComment

def get_model():
    return ThreadedComment


def get_form():
    return CommentFormWithSpamish
