from sqlalchemy import Column,String,Integer,Boolean,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Job (Base):
    __tablename__="jobs"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String, nullable=False)
    description = Column(String,nullable=False)
    company = Column(String,nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    salary = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", backref="jobs")

