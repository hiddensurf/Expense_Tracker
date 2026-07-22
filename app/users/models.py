from sqlmodel import SQLModel
from typing import TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import SecretStr
from sqlalchemy import Column,DateTime,func
from typing import List
if TYPE_CHECKING:
    from app.purchases.models import PurchaseDB
class UserBase(SQLModel):
    fullname:str | None = Field(max_length=70,default=None)
    username:str = Field(min_length=3,max_length=30,unique=True)
class UserDB(UserBase,table=True):
    __tablename__="userdb"
    id: int|None =Field(primary_key=True,default=None)
    hashed_password:str
    created_at:datetime | None =Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ))
    updated_at:datetime | None = None
    purchases:List["PurchaseDB"] = Relationship(back_populates="user",sa_relationship_kwargs={"cascade":"all,delete-orphan"})
    disabled:bool|None=None
class CreateUser(UserBase):
    password:SecretStr = Field(min_length=15)
class UserPublic(UserBase):
    id: int
class UpdateUser(SQLModel):
    username:str|None = Field(min_length=3,max_length=30,default=None)
    fullname:str | None = Field(max_length=70,default=None)
    password:SecretStr|None = Field(min_length=15, default=None)