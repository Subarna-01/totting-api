import uuid
import jwt
import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional, List
from app.core.settings import settings

auth_scheme = HTTPBearer()


def create_access_token(
    payload: dict, expires_delta: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    to_encode = payload.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=expires_delta
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(
    payload: dict, expires_delta: int = settings.REFRESH_TOKEN_EXPIRE_DAYS
) -> str:
    to_encode = payload.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=expires_delta
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def create_email_verification_token(
    payload: dict, expires_delta: int = settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES
) -> str:
    jti = str(uuid.uuid4())
    to_encode = payload.copy()
    to_encode.update({"jti": jti})
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=expires_delta
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def authenticate(required_roles: Optional[List[str]] = None):
    def wrapper(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        payload = decode_token(token.credentials)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        if required_roles:
            roles = payload.get("roles", [])
            if not any(role in roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have the required role to perform this operation",
                )

        return payload

    return wrapper
