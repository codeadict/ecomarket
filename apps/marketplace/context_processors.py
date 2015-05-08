# coding=utf-8
from .models import Category


def categories(*args):
    data = {}
    data.update(
        {
            'ROOTS_CATEGORIES': Category.objects.filter(parent=None).order_by("name"),
        }
    )
    return data
