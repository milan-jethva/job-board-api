from fastapi import APIRouter,Depends,UploadFile,File,HTTPException,BackgroundTasks
from app.models.application import Application
from app.schemas.application import applicationResponse,application_status
from app.db.session import get_db
from sqlalchemy.orm import Session
from typing import List
import os
from app.models.user import User
from app.core.dependencies import get_current_user
from app.models.job import Job
from app.models.application import Application
import shutil
from app.core.dependencies import require_recruiter
from app.services.email import send_application_email,send_status_update_mail

router = APIRouter(prefix="/application", tags=["Application"])


upload_dir = "uploads/resumes"
os.makedirs(upload_dir,exist_ok=True)

@router.post("/jobs/{job_id}/apply",response_model=applicationResponse)
def apply_job(
    job_id:int,
    background_task:BackgroundTasks,
    resume: UploadFile = File(...),
    db:Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    job_query = db.query(Job).filter(Job.id == job_id).first()
    if not job_query:
        raise HTTPException(status_code=404,detail="job does not found")
    
    already_applied = db.query(Application).filter (
        Application.job_id ==job_id,
        Application.application_id == current_user.id
    ).first()
    if already_applied:
        raise HTTPException(status_code=400, detail="Already applied")
    
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")
    
    file_path = f"{upload_dir}/{current_user.id}_{job_id}_{resume.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    application = Application(
        job_id=job_id,
        application_id=current_user.id,
        resume_path=file_path
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    
    background_task.add_task(
        send_application_email,
        current_user.email,
        job_query.title
    )

    return application

@router.get("/me",response_model=List[applicationResponse])
def my_application(
    db:Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    return db.query(Application).filter(Application.application_id == current_user.id).all()


@router.delete("/{application_id}")
def withdraw(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    app = db.query(Application).filter(
        Application.id == application_id,
        Application.application_id == current_user.id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    db.commit()
    return {"message": "Application withdrawn"}

@router.get("/jobs/{job_id}", response_model=List[applicationResponse])
def job_applicants(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter)
):
    job = db.query(Job).filter(Job.id == job_id, Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not yours")
    return db.query(Application).filter(Application.job_id == job_id).all()

@router.put("/{application_id}/status", response_model=applicationResponse)
def update_status(
    application_id: int,
    background_tasks:BackgroundTasks,
    status_data: application_status,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter)
):
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = status_data
    db.commit()
    
    db.refresh(app)
    background_tasks.add_task(
        send_status_update_mail,
        app.applicant.email,  
        app.job.title,         
        status_data  
    )
    return app