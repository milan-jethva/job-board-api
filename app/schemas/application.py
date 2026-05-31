from pydantic import BaseModel
from app.models.application import application_status

class applicationResponse(BaseModel):
    id: int
    job_id: int
    application_id: int
    resume_path: str
    status: application_status

    model_config = {"from_attributes": True}

class StatusUpdate(BaseModel):
    status: application_status