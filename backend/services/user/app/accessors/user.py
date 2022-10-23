from typing import Any

from pydantic import EmailStr

from orm.user import UserModel
from structures.named_tuples import attribute


async def create_user(email: EmailStr,
                      username: str,
                      password: str) -> UserModel:
    user = await UserModel.create(email=email,
                                  username=username,
                                  password=password)

    return user


async def update_user(user: UserModel, values: dict) -> None:
    await user.update_from_dict(data=values)
    await user.save()


async def get_user_by(attr: attribute, value: Any) -> UserModel:
    __filter = {
        attr.filter.name: value
    }

    user = await UserModel.get_or_none(**__filter)

    return user
