from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    full_name: str
    bio: str | None = None
    skills: str | None = None
    travel_preferences: str | None = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

