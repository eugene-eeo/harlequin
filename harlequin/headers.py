from collections import OrderedDict
from .utils import want_unicode


class UnicodeDict(OrderedDict):
    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self,
                                want_unicode(key),
                                want_unicode(value))
