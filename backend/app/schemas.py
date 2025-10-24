from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRequest(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    role: str 
    password: str = Field(min_length=6)
    
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="New username")
    email: Optional[str] = Field(None, description="New email")
    role: Optional[str] = Field(None, description="New role")
    password: Optional[str] = Field(None, description="Current password (required if changing password)")
    new_password: Optional[str] = Field(None, description="New password (required if changing password)")
 

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
   
    
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
  
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class PasswordVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)