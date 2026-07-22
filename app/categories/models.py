from sqlmodel import SQLModel
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column,DateTime,func
class CategoryBase(SQLModel):
    category_name:str=Field(max_digits=50)
class CategoryDB(SQLModel, table=True):
    __tablename__="categories"
    category_id:int | None = Field(primary_key=True,default= None)
    category_name:str = Field(max_digits=50,unique=True,nullable=False)
    created_at:datetime|None=Field(sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
    ))
class CategoryUpdate(SQLModel):
    updated_at:datetime|None=Field(sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
    ))