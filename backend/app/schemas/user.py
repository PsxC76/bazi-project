from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class UserRegister(BaseModel):
    username: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("账号只能包含字母、数字、下划线")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("密码只能包含字母、数字、下划线")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    bio: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class EmailBindRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("请输入正确的邮箱地址")
        return v


class EmailVerifyRequest(BaseModel):
    email: str
    code: str = Field(..., min_length=6, max_length=6)
