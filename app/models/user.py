from sqlalchemy import Column, String,Integer,Boolean,Enum
from app.db.base import Base 
import enum

class UserRole(str,enum.Enum):
    admin="admin"
    recruiter = "recruiter"
    applicant = "applicant"

class User(Base):
    __tablename__= "users"
    id = Column(Integer , primary_key=True, index=True)
    email = Column(String, unique=True , nullable=False,index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String,nullable=False)
    role = Column(Enum(UserRole),default=UserRole.applicant)
    is_active =Column(Boolean,default=True)

