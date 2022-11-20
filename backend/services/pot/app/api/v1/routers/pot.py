from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import PotModel
from schemas import integration, pot
from utils.decorators import admin_required

router = APIRouter()


@router.post(
    path=".me",
    response_description="User balance",
    response_model=pot.PotSchema,
    status_code=status.HTTP_201_CREATED,
)
async def me(
    user: integration.IntegrationUserSchema = Depends(
        tools.store.integration_user_accessor.get_user
    ),
    session: AsyncSession = Depends(depends.get_session),
) -> pot.PotSchema:
    async with session.begin_nested() as nested_session:
        user = await tools.store.user_accessor.create_user(
            session=nested_session.session,
            user_id=user.id,
        )
        pot = await tools.store.pot_accessor.create_pot(
            session=nested_session.session,
            user=user,
        )

    return pot


@router.put(
    path=".update/{user_id}",
    response_description="User balance",
    response_model=pot.PotSchema,
    status_code=status.HTTP_200_OK,
)
@admin_required(target="api_token")
async def update(
    data: pot.PotUpdateSchema,
    api_token: str = Query(...),
    user: integration.IntegrationUserViewSchema = Depends(
        tools.store.integration_user_accessor.get_user_by_id
    ),
    session: AsyncSession = Depends(depends.get_session),
) -> pot.PotSchema:
    pot = await tools.store.pot_accessor.get_pot_by(
        session=session,
        where=(PotModel.user_id == user.id),
    )
    if not pot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pot for user {user.id=} not found on server",
        )
    async with session.begin_nested() as nested_session:
        await tools.store.pot_accessor.update_pot(
            session=nested_session.session,
            pot_id=pot.id,
            pot=data.pot,
        )

    return pot
