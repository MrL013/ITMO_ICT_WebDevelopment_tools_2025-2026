from sqlalchemy.orm import Session

from app.models import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


def get_profile_by_user_id(db: Session, user_id: int) -> Profile | None:
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_or_update_profile(db: Session, user_id: int, profile_in: ProfileCreate | ProfileUpdate) -> Profile:
    profile = get_profile_by_user_id(db, user_id)
    if profile is None:
        profile = Profile(user_id=user_id, **profile_in.model_dump())
        db.add(profile)
    else:
        for field, value in profile_in.model_dump().items():
            setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile

