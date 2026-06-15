from fastapi import APIRouter

from app.api.v1.endpoints import auth, messages, parser, profiles, trips, users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(profiles.router)
api_router.include_router(trips.router)
api_router.include_router(messages.router)
api_router.include_router(parser.router)
