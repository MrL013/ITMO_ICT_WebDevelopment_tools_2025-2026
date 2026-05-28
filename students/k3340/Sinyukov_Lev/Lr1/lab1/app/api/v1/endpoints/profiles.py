from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.profile import create_or_update_profile, get_profile_by_user_id
from app.models import User
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/me", response_model=ProfileRead)
def read_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ProfileRead:
    profile = get_profile_by_user_id(db, current_user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileRead.model_validate(profile)


@router.post("/me", response_model=ProfileRead)
def create_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProfileRead:
    profile = create_or_update_profile(db, current_user.id, profile_in)
    return ProfileRead.model_validate(profile)


@router.put("/me", response_model=ProfileRead)
def update_profile(
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProfileRead:
    profile = create_or_update_profile(db, current_user.id, profile_in)
    return ProfileRead.model_validate(profile)

