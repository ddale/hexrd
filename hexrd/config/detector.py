import os

from .config import Config, Parameter
from .validators import is_int, is_str, is_str_or_none, path_exists_or_none


def is_pixel_size(key, val):
    if isinstance(val, (str, int)):
        val = float(val)
    if isinstance(val, float):
        return [val, val]
    try:
        if len(val) == 1:
            val = val[0]
            return [val, val]
        elif len(val) == 2:
            return val
    except:
        pass
    raise RuntimeError(
        '"%s" expects a float or list of two floats, received incompatible'
        ' type "%s" with val "%s"' % (key, type(val), val)
        )



class Detector(Config):

    parameters = Parameter('detector:parameters', is_str, is_str)

    parameters_old = Parameter(
        'detector:parameters_old',
        path_exists_or_none,
        is_str_or_none,
        default=None
        )

    @property
    def pixels(self):
        return Pixels(self._cfg)



class Pixels(Config):

    columns = Parameter('detector:pixels:columns', is_int, is_int)

    rows = Parameter('detector:pixels:rows', is_int, is_int)

    size = Parameter('detector:pixels:size', is_pixel_size, is_pixel_size)
