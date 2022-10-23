from enum import Enum


class FilterPathEnum(str, Enum):
    id = 'id'
    username = 'username'


class FilterEnum(str, Enum):
    id = 'id'
    email = 'email'
    username = 'username'
