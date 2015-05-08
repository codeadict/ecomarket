import inspect

from . import validators


def get_validators():
    classes = []
    for name, cls in inspect.getmembers(validators, inspect.isclass):
        if issubclass(cls, validators.BaseValidator) and cls != validators.BaseValidator:
            classes.append(cls())
    return classes


def run_validators(value):
    for validator in get_validators():
        validator(value)
    return value
