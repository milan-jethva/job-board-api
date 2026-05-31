from app.db.base import Base
from sqlalchemy import Enum,Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
import enum

class application_status(str, enum.Enum):
    pending="pending"
    accepted="accepted"
    reviewed= "reviewed"
    rejected="rejected"

class Application(Base):
    __tablename__="applications"
    id = Column(Integer, primary_key=True,index=True) 
    job_id= Column(Integer , ForeignKey("jobs.id"),nullable=False)
    application_id =Column(Integer,ForeignKey("users.id"),nullable=False)
    resume_path = Column(String,nullable=False)
    status = Column(Enum(application_status),default=application_status.pending)
    job = relationship("Job", backref="applications")
    applicant = relationship("User", backref="applications")