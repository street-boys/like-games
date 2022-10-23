from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField


class PotModel(Model):
    id = BigIntField(pk=True)

    user_id = BigIntField(null=False, unique=True)

    pot = BigIntField(default=15000)


pot_schema_out = pydantic_model_creator(PotModel,
                                        name='PotSchemaOut')

pot_schema_in = pydantic_model_creator(PotModel,
                                       name='PotSchemaIn',
                                       exclude=('id', 'user_id',))
