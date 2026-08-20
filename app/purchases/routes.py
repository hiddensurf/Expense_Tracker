from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, BackgroundTasks
from sqlmodel import select,func
from datetime import datetime
from app.purchases.functions import parse_csv
from typing import Annotated
from app.users.models import UserDB
from app.categories.models import CategoryDB
from app.auth.security import get_current_user_active,SessionDep
from app.purchases.models import PurchasePerMonth,PurchaseCreate,PurchaseDB,PurchasePublic,PurchaseUpdate,PurchasePerCategory,ExpenseQueries
router = APIRouter(dependencies=[Depends(get_current_user_active)])
@router.get("/purchases/me",response_model=list[PurchasePublic])
def get_purchases(session:SessionDep,queries:Annotated[ExpenseQueries,Depends()],user:UserDB=Depends(get_current_user_active)):
    statement = select(PurchaseDB).where(PurchaseDB.user_id == user.id)
    if queries.purchased_in_or_before is not None:
        statement=statement.where(PurchaseDB.purchased_at<=queries.purchased_in_or_before)
    if queries.purchased_in_or_after is not None:
        statement = statement.where(PurchaseDB.purchased_at>=queries.purchased_in_or_after)
    if queries.min_amount is not None:
        statement=statement.where(PurchaseDB.amount>=queries.min_amount)
    if queries.max_amount is not None:
        statement = statement.where(PurchaseDB.amount<=queries.max_amount)
    if queries.entered_in_or_before is not None:
        dt = datetime.combine(queries.entered_in_or_before,datetime.max.time())
        statement = statement.where(PurchaseDB.entered_at<=dt)
    if queries.entered_in_or_after is not None:
        dt = datetime.combine(queries.entered_in_or_after,datetime.min.time())
        statement = statement.where(PurchaseDB.entered_at>=dt)
    if queries.item_name:
        statement = statement.where(PurchaseDB.item_name.ilike(f"%{queries.item_name}%"))
    if queries.category_id is not None:
        statement = statement.where(PurchaseDB.category_id == queries.category_id)
    if queries.purchase_id is not None:
        statement = statement.where(PurchaseDB.purchase_id == queries.purchase_id)
    result = session.exec(statement).all()
    return result
@router.get("/purchases/me/{purchase_id}",response_model=PurchasePublic)
def get_purchase(session:SessionDep, purchase_id:int,user:UserDB=Depends(get_current_user_active)):
    purchase=session.exec(select(PurchaseDB).where(PurchaseDB.purchase_id == purchase_id , PurchaseDB.user_id == user.id)).first()
    if purchase is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="purchase not found")
    return purchase
@router.post("/purchases/me", response_model=PurchasePublic)
def add_purchase(session:SessionDep,purchase:PurchaseCreate,user:UserDB=Depends(get_current_user_active)):
    db_purchase=PurchaseDB(**purchase.model_dump(),user_id=user.id)
    session.add(db_purchase)
    session.commit()
    session.refresh(db_purchase)
    return db_purchase
@router.patch("/purchases/me/{purchase_id}", response_model=PurchasePublic)
def update_purchase(session:SessionDep,update_purchase:PurchaseUpdate,purchase_id:int,user:UserDB=Depends(get_current_user_active)):
    purchase_db=session.exec(select(PurchaseDB).where(PurchaseDB.user_id == user.id,PurchaseDB.purchase_id==purchase_id)).first()
    if purchase_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="purchase not found")
    purchase_model=update_purchase.model_dump(exclude_unset=True)
    purchase_db.sqlmodel_update(purchase_model)
    session.add(purchase_db)
    session.commit()
    session.refresh(purchase_db)
    return purchase_db
@router.delete("/purchases/me/{purchase_id}")
def delete_purchase(purchase_id:int,session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    purchase_db=session.exec(select(PurchaseDB).where(PurchaseDB.purchase_id == purchase_id, PurchaseDB.user_id == user.id)).first()
    if purchase_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="purchase not found")
    session.delete(purchase_db)
    session.commit()
    return {"ok":True}
@router.get("/purchases/summary")
def get_summary(session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    month = func.date_trunc("month",PurchaseDB.purchased_at)
    total=func.sum(PurchaseDB.amount).label("total")
    stmnt1 = select(PurchaseDB.category_id,
                    CategoryDB.category_name,
                    total).join(CategoryDB).where(PurchaseDB.user_id==user.id).group_by(CategoryDB.category_name,PurchaseDB.category_id)
    stmnt2 = select(month.label("month"),
                    total).where(PurchaseDB.user_id == user.id).group_by(month).order_by(month)
    stmnt3 = select(PurchaseDB.category_id,CategoryDB.category_name,total).join(CategoryDB).where(PurchaseDB.user_id == user.id).group_by(PurchaseDB.category_id,CategoryDB.category_name).order_by(func.sum(PurchaseDB.amount).desc()).limit(3)
    rows1 = session.exec(stmnt1).all()
    expense_per_category =[PurchasePerCategory(category_id=row[0],category_name=row[1],total=row[2]) for row in rows1]
    rows2=session.exec(stmnt2).all()
    expense_per_month=[PurchasePerMonth(month=row[0],total=row[1]) for row in rows2]
    rows3 = session.exec(stmnt3).all()
    top_3_expense = [PurchasePerCategory(category_id=row[0],category_name=row[1],total=row[2]) for row in rows3]
    return {"expense per month":expense_per_month,"expense per category":expense_per_category,"top three categories":top_3_expense}
@router.post("/purchases/import")
async def add_purchases(csv_file:UploadFile,background_task:BackgroundTasks,session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    background_task.add_task(parse_csv,csv_file,session,user)
    return {"message":"Purchases added"}