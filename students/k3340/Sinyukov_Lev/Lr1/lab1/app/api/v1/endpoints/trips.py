from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.trip import (
    add_trip_participant,
    create_trip,
    delete_trip,
    get_participant_link,
    get_trip,
    list_trips,
    search_trips,
    update_participant_status,
    update_trip,
)
from app.models import User
from app.schemas.trip import (
    TripCreate,
    TripParticipantCreate,
    TripParticipantUpdate,
    TripRead,
    TripReadDetailed,
    TripSearchQuery,
    TripUpdate,
)

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/", response_model=TripRead, status_code=status.HTTP_201_CREATED)
def create_trip_endpoint(
    trip_in: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TripRead:
    trip = create_trip(db, current_user.id, trip_in)
    return TripRead.model_validate(trip)


@router.get("/", response_model=list[TripReadDetailed])
def list_trips_endpoint(db: Session = Depends(get_db)) -> list[TripReadDetailed]:
    trips = list_trips(db)
    return [TripReadDetailed.model_validate(trip) for trip in trips]


@router.get("/{trip_id}", response_model=TripReadDetailed)
def get_trip_endpoint(trip_id: int, db: Session = Depends(get_db)) -> TripReadDetailed:
    trip = get_trip(db, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripReadDetailed.model_validate(trip)


@router.put("/{trip_id}", response_model=TripRead)
def update_trip_endpoint(
    trip_id: int,
    trip_in: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TripRead:
    trip = get_trip(db, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can update trip")
    updated = update_trip(db, trip, trip_in)
    return TripRead.model_validate(updated)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip_endpoint(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    trip = get_trip(db, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can delete trip")
    delete_trip(db, trip)


@router.post("/{trip_id}/join", status_code=status.HTTP_201_CREATED)
def join_trip(
    trip_id: int,
    data: TripParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    trip = get_trip(db, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if get_participant_link(db, trip_id, current_user.id):
        raise HTTPException(status_code=400, detail="Join request already exists")
    add_trip_participant(db, trip_id, current_user.id, data.note)
    return {"message": "Join request created"}


@router.patch("/{trip_id}/participants/{user_id}")
def manage_participant_status(
    trip_id: int,
    user_id: int,
    data: TripParticipantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    trip = get_trip(db, trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can manage participants")
    link = get_participant_link(db, trip_id, user_id)
    if link is None:
        raise HTTPException(status_code=404, detail="Participant link not found")
    update_participant_status(db, link, data)
    return {"message": "Participant status updated"}


@router.post("/search", response_model=list[TripReadDetailed])
def search_trips_endpoint(query: TripSearchQuery, db: Session = Depends(get_db)) -> list[TripReadDetailed]:
    trips = search_trips(db, query)
    return [TripReadDetailed.model_validate(trip) for trip in trips]

