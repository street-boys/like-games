from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.pot import PotModel
from schemas.integration.user import UserSchema
from schemas.pot import PotSchema, PotUpdateSchema
from utils.decorators import admin_required

router = APIRouter()


@router.post(
    path=".me",
    response_description="User balance",
    response_model=PotSchema,
    status_code=status.HTTP_201_CREATED,
)
async def me(
    user: UserSchema = Depends(store.integration_user_accessor.get_user),
    session: AsyncSession = Depends(get_session),
) -> PotSchema:
    async with session.begin_nested() as nested_session:
        pot = await store.pot_accessor.create_pot(
            session=nested_session.session,
            user_id=user.id,
        )

    return pot


@router.put(
    path=".update/{user_id}",
    response_description="User balance",
    response_model=PotSchema,
    status_code=status.HTTP_200_OK,
)
@admin_required(target="api_token")
async def update(
    data: PotUpdateSchema,
    api_token: str = Query(...),
    user: UserSchema = Depends(store.integration_user_accessor.get_user_by_id),
    session: AsyncSession = Depends(get_session),
) -> PotSchema:
    pot = await store.pot_accessor.get_pot_by(
        session=session,
        where=(PotModel.user_id == user.id),
    )
    if not pot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pot for user {user.id=} not found on server",
        )
    async with session.begin_nested() as nested_session:
        await store.pot_accessor.update_pot(
            session=nested_session.session,
            pot_id=pot.id,
            pot=data.pot,
        )

    return pot
