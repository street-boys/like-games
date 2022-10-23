from typing import Any

from orm.pot import PotModel
from structures.named_tuples import attribute


async def create_pot(user_id: int) -> PotModel:
    pot = await PotModel.get_or_create(id=user_id, user_id=user_id)

    return pot[0]


async def update_pot(pot: PotModel,
                     data: dict) -> None:
    await pot.update_from_dict(data=data)
    await pot.save()


async def get_pot_by(attr: attribute, value: Any) -> PotModel:
    __filter = {
        attr.filter.name: value
    }

    pot = await PotModel.get_or_none(**__filter)

    return pot
