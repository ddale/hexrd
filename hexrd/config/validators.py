import os



def default_validator(key, val):
    return val


def is_str(key, val):
    if isinstance(val, str):
        return val
    try:
        return str(val)
    except:
        raise TypeError(
            '"%s" expects a string, received incompatible type "%s" with val'
            ' "%s"' % (key, type(val), val)
            )

def is_str_or_none(key, val):
    if val is None:
        return
    return is_str(key, val)


def is_int(key, val):
    if isinstance(val, int):
        return val
    try:
        return int(val)
    except:
        raise TypeError(
            '"%s" expects an int, received incompatible type "%s" with val'
            ' "%s"' % (key, type(val), val)
            )


def is_float(key, val):
    if isinstance(val, float):
        return val
    try:
        return float(val)
    except:
        raise TypeError(
            '"%s" expects an float, received incompatible type "%s" with val'
            ' %s' % (key, type(val), val)
            )


def path_exists(key, val):
    if not os.path.exists(val):
        raise IOError(
            '"%s": "%s" does not exist' % (key, val)
            )
    return val


def path_exists_or_none(key, val):
    if val is None:
        return val
    return path_exists(key, val)
