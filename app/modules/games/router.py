from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from functools import partial
from app.core.database.dependencies import get_db
from app.core.jwt import authenticate
from app.core.settings import settings
from app.modules.games.service import GameService

router = APIRouter(prefix="/games")

game_service = GameService()


@router.get("/")
async def get_games(
    genre_id: int | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    payload: dict = Depends(authenticate()),
    db: Session = Depends(partial(get_db, settings.GAMES_DB)),
) -> JSONResponse:
    return await game_service.get_games(genre_id, offset, limit, db)
