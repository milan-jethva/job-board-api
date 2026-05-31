from pydantic import BaseModel , EmailStr
from app.models.user import UserRole

class UserIn (BaseModel):
    email : EmailStr
    password : str
    full_name:str
    role : UserRole = UserRole.applicant

class UserResponse(BaseModel):
    email:str
    full_name:str
    role:UserRole
    is_active:bool

    model_config={"from_attributes":True}

class Token(BaseModel):
    access_token:str
    token_type:str

class LoginRequest(BaseModel):
    email: EmailStr
    password : str

