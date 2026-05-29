from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database.base import GAMES_DB_BASE


class GameGenre(GAMES_DB_BASE):
    __tablename__ = "game_genres"
    __table_args__ = {"extend_existing": True}

    _id = Column("_id", Integer, primary_key=True, autoincrement=True)
    genre_name = Column("genre_name", String, nullable=False)
    created_by = Column("created_by", UUID(as_uuid=True))
    created_at = Column(
        "created_at", TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_by = Column("updated_by", UUID(as_uuid=True))
    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_by = Column("deleted_by", UUID(as_uuid=True))
    deleted_at = Column("deleted_at", TIMESTAMP(timezone=True))

    games = relationship("Game", back_populates="genre")


class Game(GAMES_DB_BASE):
    __tablename__ = "games"
    __table_args__ = {"extend_existing": True}

    _id = Column("_id", Integer, primary_key=True, autoincrement=True)
    genre_id = Column(
        "genre_id",
        Integer,
        ForeignKey("game_genres._id", ondelete="RESTRICT"),
        nullable=False,
    )
    game_name = Column("game_name", String, nullable=False)
    display_image_url = Column("display_image_url", String, nullable=False)
    created_by = Column("created_by", UUID(as_uuid=True))
    created_at = Column(
        "created_at", TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_by = Column("updated_by", UUID(as_uuid=True))
    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_by = Column("deleted_by", UUID(as_uuid=True))
    deleted_at = Column("deleted_at", TIMESTAMP(timezone=True))

    genre = relationship("GameGenre", back_populates="games")
