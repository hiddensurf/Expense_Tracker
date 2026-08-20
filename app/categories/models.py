from sqlmodel import SQLModel
from datetime import datetime
from sqlmodel import SQLModel, Field,Relationship
from sqlalchemy import Column,DateTime,func
from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.purchases.models import PurchaseDB
class CategoryBase(SQLModel):
    category_name:str=Field(max_length=50)
class CategoryDB(SQLModel, table=True):
    __tablename__="categories"
    category_id:int | None = Field(primary_key=True,default= None)
    category_name:str = Field(max_length=50,unique=True,nullable=False)
    created_at:datetime=Field(sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
    ))
    updated_at:datetime=Field(sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
    ))
    purchases:List["PurchaseDB"]=Relationship(sa_relationship_kwargs={"passive_deletes":True})
class CategoryCreate(CategoryBase):
    pass
class CategoryPublic(CategoryBase):
    category_id:int
    category_name:str
class CategoryUpdate(SQLModel):
    category_name:str