from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import cast, String
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.jwt import create_access_token, create_refresh_token
from app.core.security import hash_password, verify_password
from app.models.users.models import User, UserContact
from app.modules.users.enum import UserStatus
from app.modules.users.schemas import UserCreate, UserLogin, UserContactAdd


class UserAccountService:
    def __init__(self) -> None:
        pass

    async def get_user_by_id(self, user_id: str, db: Session) -> JSONResponse:
        try:
            user = (
                db.query(User)
                .filter(
                    cast(User.user_id, String) == user_id,
                    User.status == UserStatus.ACTIVE.value,
                    User.deleted_at.is_(None),
                )
                .first()
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            
            contact = next(
                (
                    contact
                    for contact in user.contacts
                    if contact.deleted_at is None
                ),
                None,
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "success",
                    "data": {
                        "user_id": str(user.user_id),
                        "email": user.email,
                        "is_email_verified": user.is_email_verified,
                        "is_organizer": user.is_organizer,
                        "created_at": str(user.created_at),
                        "contact": (
                            {
                                "dial_code": contact.dial_code,
                                "mobile_number": contact.mobile_number,
                                "is_mobile_number_verified": contact.is_mobile_number_verified,
                            }
                            if contact
                            else None
                        ),
                    },
                },
            )

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error has occurred",
            )

    async def create(self, request_body: UserCreate, db: Session) -> JSONResponse:
        try:
            user = (
                db.query(User)
                .filter(
                    User.email == request_body.email,
                    User.deleted_at.is_(None),
                )
                .first()
            )

            if user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )

            user = User(
                email=request_body.email,
                password_hash=hash_password(request_body.password),
                is_organizer=request_body.is_organizer,
                status=UserStatus.INACTIVE.value,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "status": "success",
                    "data": {"user_id": str(user.user_id)},
                },
            )

        except HTTPException:
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )

    async def login(self, request_body: UserLogin, db: Session) -> JSONResponse:
        try:
            user = (
                db.query(User)
                .filter(
                    User.email == request_body.email,
                    User.deleted_at.is_(None),
                )
                .first()
            )

            if not user or not verify_password(
                request_body.password, user.password_hash
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            if user.status == UserStatus.INACTIVE.value or not user.is_email_verified:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account not active",
                )

            user.last_login_at = datetime.now(timezone.utc)

            db.commit()

            token_payload = {
                "user_id": str(user.user_id),
                "email": user.email,
            }

            access_token = create_access_token(token_payload)
            refresh_token = create_refresh_token(token_payload)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "success",
                    "data": {
                        "token_type": "bearer",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
            )

        except HTTPException:
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error has occurred",
            )

    
    async def add_contact(self, user_id: str, request_body: UserContactAdd, db: Session) -> JSONResponse:
        try:
            contact = (
                db.query(UserContact)
                .filter(
                    cast(UserContact.user_id, String) == user_id,
                    UserContact.deleted_at.is_(None),
                )
                .first()
            )

            if contact:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Contact already added"
                )

            contact = UserContact(
                user_id=user_id,
                dial_code=request_body.dial_code,
                mobile_number=request_body.mobile_number,
                is_mobile_number_verified=True
            )

            db.add(contact)
            db.commit()
            db.refresh(contact)

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "status": "success",
                    "data": {"_id": str(contact._id)},
                },
            )

        except HTTPException:
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )
        
    async def delete_contact(self, user_id: str, db: Session) -> JSONResponse:
        try:
            contact = (
                db.query(UserContact)
                .filter(
                    cast(UserContact.user_id, String) == user_id,
                    UserContact.deleted_at.is_(None),
                )
                .first()
            )

            if not contact:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No contact found"
                )
            
            contact.deleted_at = datetime.now(timezone.utc)
            
            db.commit()

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status": "success"
                },
            )

        except HTTPException:
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred",
            )
