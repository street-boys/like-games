from enum import Enum


class ChatTypeEnum(str, Enum):
    public = 'public'
    private = 'private'


class FilterEnum(str, Enum):
    id = 'id'
    user_id = 'user_id'


class MessageTypeEnum(str, Enum):
    view = 'view'
    add = 'add'
