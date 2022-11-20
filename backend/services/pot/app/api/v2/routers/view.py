from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import PotModel
from schemas import integration, pot

router = APIRouter()


@router.get(
    path=".view/{user_id}",
    response_description="User balance",
    response_model=pot.PotSchema,
    status_code=status.HTTP_200_OK,
)
async def view_pot(
    user_id: int = Path(...), session: AsyncSession = Depends(tools.get_session)
) -> pot.PotSchema:
    pot = await tools.store.pot_accessor.get_pot_by(
        session=session,
        where=(PotModel.user_id == user_id),
    )

    if not pot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pot for user {user_id=} not found on server",
        )

    return pot


@router.get(
    path=".me.view",
    response_description="User balance",
    response_model=pot.PotSchema,
    status_code=status.HTTP_200_OK,
)
async def view_me(
    user: integration.IntegrationUserSchema = Depends(
        tools.store.integration_user_accessor.get_user
    ),
    session: AsyncSession = Depends(tools.get_session),
) -> pot.PotSchema:
    return await view_pot(user_id=user.id, session=session)
