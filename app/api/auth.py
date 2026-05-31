from fastapi import APIRouter ,Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import user
from app.db.session import get_db
from app.models import User
from app.core.security import hash_password,verify_password,create_access_token

router = APIRouter()

@router.post("/register",response_model=user.UserResponse)
def create_user(user_in : user.UserIn , db : Session= Depends(get_db)):

    existing = db.query(User).filter(user_in.email == User.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="User already exist")

    hash_pass = hash_password(user_in.password)
    user = User(**user_in.model_dump(exclude={"password"}),hashed_password=hash_pass )


    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login",response_model=user.Token)
def user_login(userLoginCred : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    userQuery  = db.query(User).filter(userLoginCred.username==User.email).first()

    if not userQuery or not verify_password(userLoginCred.password , userQuery.hashed_password):
        raise HTTPException(status_code=401 , detail="Invalid credentials")

    token = create_access_token(data = {"sub" : str(userQuery.id),"role":userQuery.role})
    return {"access_token": token, "token_type": "bearer"}