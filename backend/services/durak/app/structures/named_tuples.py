from collections import namedtuple

from .enums import FilterEnum

attribute = namedtuple('attributes', [
    'filter'
], defaults=(FilterEnum.id,))
