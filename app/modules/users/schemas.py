import re
from pydantic import BaseModel, EmailStr, constr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=6)  # type: ignore
    is_organizer: bool = False

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str):
        return value.strip().lower()


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(strip_whitespace=True, min_length=1)  # type: ignore

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str):
        return value.strip().lower()

class UserContactAdd(BaseModel):
    dial_code: constr(strip_whitespace=True, min_length=2, max_length=4) # type: ignore
    mobile_number: constr(strip_whitespace=True, max_length=14) # type: ignore
    is_mobile_number_verified: bool = False

    @field_validator("dial_code")
    @classmethod
    def validate_dial_code(cls, value: str) -> str:
        if not re.fullmatch(r"\+\d{1,3}", value):
            raise ValueError(
                "Dial code must start with '+' followed by 1 to 3 digits"
            )
        return value