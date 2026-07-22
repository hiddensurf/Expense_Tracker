from fastapi import APIRouter, Depends, Query,HTTPException,status
from app.database.database import SessionDep
from typing import Annotated
from sqlmodel import select
from app.users.models import UserPublic, UserDB, UpdateUser
from app.auth.security import get_current_user_active,hash_password
router = APIRouter(dependencies=[Depends(get_current_user_active)])
@router.get("/users",response_model=list[UserPublic])
def get_users(session:SessionDep,offset:int|None=None,limit:Annotated[int,Query(le=100)]=100):
    users=session.exec(select(UserDB).limit(limit).offset(offset))
    return users
@router.get("/users/{user_id}",response_model=UserPublic)
def get_user(user_id:int,session:SessionDep):
    user = session.exec(select(UserDB).where(UserDB.id ==user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    return user
@router.patch("/users/me",response_model=UserPublic)
def update_user(update_data:UpdateUser,session:SessionDep,db_user:UserDB=Depends(get_current_user_active)):
    if update_data.username is not None and update_data.username != db_user.username:
        existing_username=session.exec(select(UserDB).where(UserDB.username == update_data.username)).first()
        if existing_username :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already exists")
    user_model=update_data.model_dump(exclude_unset=True)
    if update_data.password is not None:
        user_model.pop("password",None)
        user_model["hashed_password"] = hash_password(update_data.password.get_secret_value())
    db_user.sqlmodel_update(user_model)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
@router.delete("/users/me")
def delete_user(session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    session.delete(user)
    session.commit()
    return{"ok":True}
@router.get("/users/me/purchases")
def get_purchases(db_user:UserDB=Depends(get_current_user_active)):
    purchases=db_user.purchases
    return purchases
