from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas import job
from typing import Annotated,List,Optional
from app.db.session import get_db
from app.models.job import Job
from app.core.dependencies import get_current_user,require_recruiter
from app.models.user import User

router =APIRouter(prefix="/jobs", tags=["jobs"])

#public job that anyone can view with filters

@router.get("/",response_model=List[job.JobResponse])
def get_job(
    skip : int = 0 ,
    location : Optional[str] =None,
    title : Optional[str] =None,
    limit : int =10,
    db:Session = Depends(get_db)
):
    query = db.query(Job).filter(Job.is_active==True)
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if title:
        query = query.filter(Job.title.ilike(f"%{title}%"))
    return query.offset(skip).limit(limit).all()

#get job by id
@router.get("/{job_id}",response_model=job.JobResponse)
def get_job_id(job_id : int , db:Session= Depends(get_db)) :
    get_job_query = db.query(Job).filter(Job.id == job_id).first()
    if not get_job_query:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return get_job_query


#recuirter only
@router.post("/", response_model=job.JobResponse)
def create_job(
    job_input: job.jobsCreate,
    db:Session = Depends(get_db),
    get_current_user: User = Depends(require_recruiter)
):
    job_in = Job(**job_input.model_dump(), owner_id = get_current_user.id)

    db.add(job_in)
    db.commit()
    db.refresh(job_in)
    return job_in

@router.put("/{job_id}",response_model=job.JobResponse)
def job_update(
    job_id:int,
    job_input:job.JobUpdate,
    db:Session = Depends(get_db),
    get_current_user: User = Depends(require_recruiter)
):
    job_query = db.query(Job).filter(Job.id == job_id , Job.owner_id == get_current_user.id).first()
    if not job_query:
        raise HTTPException(status_code=404 ,detail="Job not found")
    for key,value in job_input.model_dump(exclude_unset=True).items():
        setattr(job_query,key, value)
    
    db.commit()
    db.refresh(job_query)
    return job_query

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter)
):
    job = db.query(Job).filter(Job.id == job_id, Job.owner_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"} 

