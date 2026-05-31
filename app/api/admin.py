from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserResponse
from app.schemas.job import JobResponse
from app.db.session import get_db
from app.models.user import User
from app.core.dependencies import require_admin
from app.models.job import Job

router=APIRouter(
    prefix="/admin" , tags=["admin"]
)

#get all current user by only admin
@router.get("/users",response_model=List[UserResponse])
def get_all_user(
    db:Session = Depends(get_db),
    current_user:User =Depends(require_admin)
):
    user_query = db.query(User).all()
    return user_query


@router.put("/users/{user_id}/ban")
def ban_user(user_id:int, db:Session = Depends(get_db),
    current_user:User =Depends(require_admin)
):
    user_query=db.query(User).filter(User.id == user_id).first()
    if not user_query:
        raise HTTPException(status_code=404,detail="user not found")
    
    user_query.is_active=False
    db.commit()
    db.refresh(user_query)
    return user_query

@router.put("/users/{user_id}/activate")
def ban_user(user_id:int, db:Session = Depends(get_db),
    current_user:User =Depends(require_admin)
):
    user_query=db.query(User).filter(User.id == user_id).first()
    if not user_query:
        raise HTTPException(status_code=404,detail="user not found")
    
    user_query.is_active=True
    db.commit()
    db.refresh(user_query)
    return user_query



@router.get("/jobs", response_model=List[JobResponse])
def get_all_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Job).all()



@router.delete("/jobs/{job_id}")
def delete_any_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted by admin"}
