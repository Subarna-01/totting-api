from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from functools import partial
from app.core.database.dependencies import get_db
from app.core.jwt import authenticate
from app.core.settings import settings
from app.modules.users.schemas import UserCreate, UserLogin, UserContactAdd
from app.modules.users.service import UserAccountService

router = APIRouter(prefix="/users")

user_account_service = UserAccountService()


@router.get("/accounts/profile")
async def get_user_by_id(
    payload: dict = Depends(authenticate()),
    db: Session = Depends(partial(get_db, settings.USERS_DB)),
) -> JSONResponse:
    return await user_account_service.get_user_by_id(payload.get("user_id"), db)


@router.post("/accounts/create")
async def create(
    request_body: UserCreate,
    db: Session = Depends(partial(get_db, settings.USERS_DB)),
) -> JSONResponse:
    return await user_account_service.create(request_body, db)


@router.post("/accounts/login")
async def login(
    request_body: UserLogin,
    db: Session = Depends(partial(get_db, settings.USERS_DB)),
) -> JSONResponse:
    return await user_account_service.login(request_body, db)

@router.post("/accounts/add-contact")
async def add_contact(
    request_body: UserContactAdd,
    payload: dict = Depends(authenticate()),
    db: Session = Depends(partial(get_db, settings.USERS_DB)),
) -> JSONResponse:
    return await user_account_service.add_contact(payload.get("user_id"), request_body, db)

@router.delete("/accounts/delete-contact")
async def delete_contact(
    payload: dict = Depends(authenticate()),
    db: Session = Depends(partial(get_db, settings.USERS_DB)),
) -> JSONResponse:
    return await user_account_service.delete_contact(payload.get("user_id"), db)