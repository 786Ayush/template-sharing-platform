from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TemplateBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class TemplateResponse(TemplateBase):
    id: Optional[str] = Field(None, alias="_id")
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PaymentIntent(BaseModel):
    amount: int
    currency: str = "usd"
    template_id: str

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
