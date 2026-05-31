from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from app.config import settings
from app.db.session import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token : str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    try:
        payload= jwt.decode(token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id : str =payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401 , detail="invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="user is not active")
    return user



def require_recruiter(current_user : User = Depends(get_current_user)):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403,detail="recruiter only")
    return current_user

    

def require_admin(current_user : User =Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="admin only")
    return current_user
