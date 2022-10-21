from typing import Any

from orm.profile import ProfileModel
from structures.named_tuples import attribute


async def create_profile(user_id: int) -> ProfileModel:
    profile = await ProfileModel.get_or_create(id=user_id, user_id=user_id)

    return profile[0]


async def update_profile(profile: ProfileModel,
                         data: dict) -> None:
    await profile.update_from_dict(data=data)
    await profile.save()


async def get_profile_by(attr: attribute, value: Any) -> ProfileModel:
    __filter = {
        attr.filter.name: value
    }

    profile = await ProfileModel.get_or_none(**__filter)

    return profile
