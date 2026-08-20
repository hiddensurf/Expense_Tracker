from typing import TYPE_CHECKING,Optional,Tuple
from sqlmodel import SQLModel
from fastapi import Query
from datetime import datetime,date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column,DateTime,func,ForeignKey
from pydantic import model_validator,BaseModel
if TYPE_CHECKING:
    from app.users.models import UserDB
class PurchaseBase(SQLModel):
    purchase_id: int|None = Field(primary_key=True, default=None)
class PurchaseDB(PurchaseBase,table=True):
    __tablename__="purchases"
    item_name: str =Field(nullable=False)
    description: str | None = None
    purchased_at:date
    amount:int
    user_id: int|None = Field(sa_column=Column(ForeignKey("userdb.id",ondelete="SET NULL"),nullable=True))
    category_id: int|None = Field(sa_column=Column(ForeignKey("categories.category_id",ondelete="SET NULL"),nullable=True))
    entered_at:datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    ))
    user:Optional["UserDB"]=Relationship(back_populates="purchases")
class PurchaseCreate(SQLModel):
    item_name:str
    description:str|None=None
    purchased_at:date
    amount:int
    category_id:int
class PurchasePublic(PurchaseBase):
    item_name:str
    description:str|None=None
    purchased_at:date
    amount:int
    category_id:int
    entered_at:datetime
class PurchaseUpdate(SQLModel):
    item_name:str|None = None
    description:str|None=None
    purchased_at:date|None=None
    amount:int|None=None
    category_id:int|None=None
class PurchasePerCategory(SQLModel):
    category_id:int
    category_name:str
    total:int
class PurchasePerMonth(SQLModel):
    month:datetime
    total:int
class ExpenseQueries(BaseModel):
    purchased_in_or_before:date|None = None
    purchased_in_or_after:date|None = None
    min_amount:int|None=None
    max_amount:int|None=None
    entered_in_or_before:date|None = None
    entered_in_or_after:date|None=None
    item_name:str|None=None
    category_id:int|None=None
    purchase_id:int|None=None
    @model_validator(mode='after')
    def validate_amounts(self):
        if self.min_amount is not None and self.max_amount is not None and self.min_amount>self.max_amount:
            raise ValueError("min amount should be less than max amount")
        if self.purchased_in_or_before is not None and self.purchased_in_or_after is not None and self.purchased_in_or_before>self.purchased_in_or_after:
            raise ValueError("'purchased_before' cannot be be a date after 'purchased_after'")
        if self.entered_in_or_before is not None and self.entered_in_or_after is not None and self.entered_in_or_before>self.entered_in_or_after:
            raise ValueError("'entered_before' cannot be a date afer 'entered_after'")
        return self



