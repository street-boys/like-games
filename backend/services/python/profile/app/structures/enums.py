from enum import Enum


class ProfileImageContentTypeEnum(str, Enum):
    gif = 'image/gif'
    png = 'image/png'
    jpeg = 'image/jpeg'

    unregistered = 'text/plain'


class FilterEnum(str, Enum):
    user_id = 'user_id'
