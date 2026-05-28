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
