from typing import TYPE_CHECKING,Optional
from sqlmodel import SQLModel
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column,DateTime,func,ForeignKey
if TYPE_CHECKING:
    from app.users.models import UserDB
class PurchaseBase(SQLModel):
    purchase_id: int|None = Field(primary_key=True, default=None)
class PurchaseDB(PurchaseBase,table=True):
    __tablename__="purchases"
    item_name: str =Field(nullable=False)
    description: str | None = None
    purchased_at:datetime
    amount:int
    user_id: int|None = Field(sa_column=Column(ForeignKey("userdb.id",ondelete="SET NULL"),nullable=True))
    category_id: int|None = Field(sa_column=Column(ForeignKey("categories.category_id",ondelete="SET NULL"),nullable=True))
    entered_at:datetime | None = Field(sa_column=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    ))
    user:Optional["UserDB"]=Relationship(back_populates="purchases")
