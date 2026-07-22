from fastapi import APIRouter, Form, Depends
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from app.auth.exceptions import credential_exception_routes
from fastapi import HTTPException, status
from app.users.models import UserPublic,CreateUser,UserDB
from app.database.database import SessionDep
from fastapi import HTTPException,status
from app.auth.models import Token
from app.auth.security import authenticate_user,hash_password,create_token,verify_password
router = APIRouter()
@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model=UserPublic)
async def signup(session:SessionDep,user:CreateUser):
    existing_username = session.exec(select(UserDB).where(UserDB.username==user.username)).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already exists")
    db_user=UserDB(**user.model_dump(exclude={"password"}),hashed_password=hash_password(user.password.get_secret_value()))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
@router.post("/token")
def login(session:SessionDep,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = authenticate_user(session=session,username=form_data.username,password=form_data.password)
    if user is None:
        raise credential_exception_routes
    data={"sub":form_data.username}
    token=create_token(data=data,exp_time=timedelta(minutes=30))
    return Token(access_token=token,token_type="bearer")