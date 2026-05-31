from pydantic import BaseModel
from typing import Optional

class jobsCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    salary: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    is_active: Optional[bool] = None

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    salary: Optional[str]
    is_active: bool
    owner_id: int

    model_config = {"from_attributes": True}

    
