from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.user import list_users
from app.models import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[UserRead]:
    users = list_users(db)
    return [UserRead.model_validate(user) for user in users]

