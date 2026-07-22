from fastapi.security import OAuth2PasswordBearer
from config import settings
from pwdlib import PasswordHash
from sqlmodel import Session,select
from app.users.models import UserDB
from typing import Annotated
from datetime import timedelta,datetime,timezone
from app.database.database import SessionDep
import jwt
from fastapi import Depends
from app.auth.exceptions import credential_exception_security, disabled_user_exception
from jwt.exceptions import InvalidTokenError
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
TIME_TO_EXPIRE=settings.time_to_expire
password_hash=PasswordHash.recommended()
DUMMY_PASSWORD = password_hash.hash("dummypassword159@")
def verify_password(password,hashed_password):
    return password_hash.verify(password,hashed_password)
def hash_password(password):
    hashed_password = password_hash.hash(password)
    return hashed_password
def get_user_from_db(session:Session,username):
    user=session.exec(select(UserDB).where(UserDB.username==username)).first()
    return user
def authenticate_user(session:SessionDep,username,password):
    user = get_user_from_db(session=session,username=username)
    if not user:
        verify_password(password,DUMMY_PASSWORD)
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user
def create_token(data:dict,exp_time:timedelta|None = None):
    to_encode=data.copy()
    if exp_time:
        exp=datetime.now(tz=timezone.utc)+exp_time
    else:
        exp=datetime.now(tz=timezone.utc)+timedelta(minutes=TIME_TO_EXPIRE)
    to_encode["exp"] = exp
    encoded_token=jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_token
def get_current_user(session:SessionDep,token=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise credential_exception_security
    except InvalidTokenError:
        raise credential_exception_security
    user = get_user_from_db(session=session,username=username)
    if user is None:
        raise credential_exception_security
    return user
def get_current_user_active(user:Annotated[UserDB,Depends(get_current_user)]):
    if user.disabled:
        raise disabled_user_exception
    return user

