from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from app.models.games.models import Game


class GameService:
    def __init__(self) -> None:
        pass

    async def get_games(
        self, genre_id: int | None, offset: int, limit: int, db: Session
    ) -> JSONResponse:
        try:
            query = (
                db.query(Game)
                .options(joinedload(Game.genre))
                .filter(
                    Game.deleted_at.is_(None),
                )
            )

            if genre_id:
                query = query.filter(Game.genre_id == genre_id)

            games = query.order_by(Game._id.asc()).offset(offset).limit(limit).all()

            data = []

            for game in games:
                data.append(
                    {
                        "_id": game._id,
                        "genre_name": game.genre.genre_name,
                        "game_name": game.game_name,
                        "display_image_url": game.display_image_url,
                    }
                )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "success", "data": data},
            )

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error has occurred",
            )
