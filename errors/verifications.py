from .exceptions import WordNetError


def verify_type(value, name, v_type):
    if not isinstance(value, v_type):
        raise TypeError("Argument '{}' has an inccorect type(expected {},got {}"
                        ")".format(name, v_type.__name__, type(value).__name__))











