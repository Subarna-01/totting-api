from sqlalchemy import (
    Boolean,
    Column,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database.base import USERS_DB_BASE


class User(USERS_DB_BASE):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = Column(
        "user_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email = Column("email", String, nullable=False)
    is_email_verified = Column("is_email_verified", Boolean, default=False)
    password_hash = Column("password_hash", String, nullable=False)
    is_organizer = Column("is_organizer", Boolean, default=False)
    status = Column("status", String(25), nullable=False)
    last_login_at = Column("last_login_at", TIMESTAMP(timezone=True))
    created_at = Column(
        "created_at", TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column("deleted_at", TIMESTAMP(timezone=True))

    contacts = relationship(
        "UserContact",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserContact(USERS_DB_BASE):
    __tablename__ = "user_contacts"
    __table_args__ = {"extend_existing": True}

    _id = Column("_id", Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    dial_code = Column("dial_code", String(4), nullable=False)
    mobile_number = Column(
        "mobile_number",
        String(14),
        nullable=False,
    )
    is_mobile_number_verified = Column(
        "is_mobile_number_verified",
        Boolean,
        default=False,
    )
    created_at = Column(
        "created_at", TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column("deleted_at", TIMESTAMP(timezone=True))

    user = relationship(
        "User",
        back_populates="contacts",
    )
