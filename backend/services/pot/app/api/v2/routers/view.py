from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.pot import PotModel
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from schemas.pot import PotSchema

view_router = APIRouter()


@view_router.get(path=".view/{user_id}", status_code=status.HTTP_200_OK)
async def view_pot(
        user_id: int = Path(...), session: AsyncSession = Depends(get_session)
) -> dict:
    pot = await store.pot_accessor.get_pot_by(
        session=session, where=(PotModel.user_id == user_id)
    )

    if not pot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pot for user {user_id=} not found on server",
        )
    pot_out = PotSchema.from_orm(pot)

    return okay_response(detail={"pot": pot_out.dict()})


@view_router.get(path=".me.view", status_code=status.HTTP_200_OK)
async def view_me(
        user: UserSchema = Depends(store.integration_user_accessor.get_user),
        session: AsyncSession = Depends(get_session)
) -> dict:
    return await view_pot(user_id=user.id, session=session)
