import logging

from .validators import default_validator

logger = logging.getLogger('hexrd.config')

class Null:
    pass
null = Null()



class Parameter(object):

    """A descriptor to validate configuration parameters

    Inputs:
      config:id:string
      getter validator
      setter validator
      default

    the validators default to no-ops, and the `default` defaults to `null`
    """

    def __init__(
            self,
            id,
            get_validator=default_validator,
            set_validator=default_validator,
            default=null
            ):
        self.id = id
        self.default = default
        self.get_validator = get_validator
        self.set_validator = set_validator


    def __get__(self, obj, type=None):
        try:
            default = self.default(obj._cfg)
        except:
            default = self.default
        return self.get_validator(
            self.id,
            obj.get(self.id, default)
            )


    def __set__(self, obj, val):
        obj[self.id] = self.set_validator(self.id, val)



class Config(object):


    def __get_section_dict(self, *args):
        res = self._cfg
        for arg in args:
            temp = res.get(arg, {})
            if temp is None:
                # intermediate block may be None, let's fix that:
                res[arg] = temp = {}
            res = temp
        return res


    def get(self, key, default=null):
        try:
            return self[key]
        except KeyError:
            if default is null:
                raise RuntimeError('%s not specified in config file')
            logger.info('%s not specified, defaulting to %s', key, default)
            return default


    def __getitem__(self, key):
        args = key.split(':')
        return self.__get_section_dict(*args[:-1])[args[-1]]


    def __setitem__(self, key, val):
        args = key.split(':')
        self.__get_section_dict(*args[:-1])[args[-1]] = val


    def __init__(self, cfg):
        self._cfg = cfg
