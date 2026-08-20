from sqlmodel import SQLModel
from typing import TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import SecretStr
from pydantic import Field as PydField
from sqlalchemy import Column,DateTime,func
from app.auth.models import Roles
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
    created_at:datetime=Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ))
    updated_at:datetime= Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False))
    purchases:List["PurchaseDB"] = Relationship(back_populates="user",sa_relationship_kwargs={"passive_deletes":True})
    user_role:str=Field(nullable=False)
    disabled:bool|None=None
class CreateUser(UserBase):
    password:SecretStr = Field(min_length=15)
    user_role: Roles = PydField(default=Roles.USER,examples=["user"])
class UserPublic(UserBase):
    id: int
class UpdateUser(SQLModel):
    username:str|None = Field(min_length=3,max_length=30,default=None)
    fullname:str | None = Field(max_length=70,default=None)
    password:SecretStr|None = Field(min_length=15, default=None)