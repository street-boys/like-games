from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import (BigIntField, BinaryField, CharEnumField,
                                  TextField)

from structures.enums import ProfileImageContentTypeEnum


class ProfileModel(Model):
    id = BigIntField(pk=True)

    user_id = BigIntField(null=False, unique=True)

    bio = TextField(default='No profile bio provided.')

    profile_image = BinaryField(null=True)
    profile_image_content_type = CharEnumField(enum_type=ProfileImageContentTypeEnum,
                                               default=ProfileImageContentTypeEnum.unregistered)


profile_schema_out = pydantic_model_creator(ProfileModel,
                                            name='ProfileSchemaOut',
                                            exclude=('profile_image', 'profile_image_content_type',))
profile_schema_in = pydantic_model_creator(ProfileModel,
                                           name='ProfileSchemaIn',
                                           exclude=('id', 'user_id', 'profile_image', 'profile_image_content_type',))
