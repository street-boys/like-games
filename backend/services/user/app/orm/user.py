from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import (BigIntField, BooleanField, CharField,
                                  DatetimeField, TextField)


class UserModel(Model):
    id = BigIntField(pk=True, index=True)

    email = CharField(max_length=200, index=True, unique=True)
    username = TextField()
    password = TextField()

    join = DatetimeField(auto_now=True)

    online = BooleanField(default=False)


user_schema_in_registration = pydantic_model_creator(UserModel,
                                                     name='UserSchemaInRegistration',
                                                     exclude=('id', 'verified', 'join', 'online',))
user_schema_in_login = pydantic_model_creator(UserModel,
                                              name='UserSchemaInLogin',
                                              exclude=('id', 'username', 'verified', 'join', 'online',))
user_schema_out = pydantic_model_creator(UserModel,
                                         name='UserSchemaOut',
                                         exclude=('password',))
user_schema_view_out = pydantic_model_creator(UserModel,
                                              name='UserSchemaViewOut',
                                              exclude=('email', 'password', 'join',))
user_schema_recovery = pydantic_model_creator(UserModel,
                                              name='UserSchemaRecovery',
                                              exclude=('id', 'username', 'password', 'join', 'online',))  # TODO: add the ability to recover an account using this scheme
