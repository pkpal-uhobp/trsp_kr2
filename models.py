from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    age: Annotated[int | None, Field(None, ge=1)]
    is_subscribed: bool = False


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserProfileSchema(BaseModel):
    username: str
    email: str
    full_name: str


class CommonHeaders(BaseModel):
    user_agent: Annotated[str, Field(..., title="User-Agent")]
    accept_language: Annotated[str, Field(..., title="Accept-Language")]
