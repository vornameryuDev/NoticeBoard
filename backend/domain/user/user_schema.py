from datetime import datetime
from multiprocessing import Value
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from starlette import status
from pydantic_core.core_schema import FieldValidationInfo




class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class Users(BaseModel):
    id: int
    username: str
    password: str
    email: str
    create_date: datetime


class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
    @field_validator('password2')
    def password_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and info.data['password1'] != v:
            raise ValueError('비밀번호가 불일치')
        return v