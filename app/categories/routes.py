from fastapi import APIRouter,Depends, Query,HTTPException,status
from app.categories.models import CategoryPublic,CategoryDB,CategoryUpdate, CategoryCreate
from app.auth.security import get_current_user_active, admin_role
from sqlmodel import select
from typing import Annotated
from app.database.database import SessionDep
router=APIRouter(dependencies=[Depends(get_current_user_active)])
@router.get("/categories",response_model=list[CategoryPublic])
def get_categories(session:SessionDep,offset:int=0,limit:Annotated[int,Query(le=100)]=100):
    categories=session.exec(select(CategoryDB).limit(limit).offset(offset)).all()
    return categories
@router.get("/categories/{category_id}",response_model=CategoryPublic)
def get_category(category_id:int,session:SessionDep):
    category=session.exec(select(CategoryDB).where(CategoryDB.category_id == category_id)).first()
    return category
@router.post("/categories",response_model=CategoryPublic)
def add_category(session:SessionDep,category:CategoryCreate,_=Depends(admin_role)):
    existing_category=session.exec(select(CategoryDB).where(CategoryDB.category_name == category.category_name)).first()
    if existing_category is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = "category name already exists")
    db_category = CategoryDB(**category.model_dump())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category
@router.patch("/categories/{category_id}",response_model=CategoryPublic)
def patch_category(update_category:CategoryUpdate,category_id:int,session:SessionDep,_=Depends(admin_role)):
    category=session.get(CategoryDB,category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="category not exists")
    category_name=update_category.category_name
    existing_name = session.exec(select(CategoryDB).where(CategoryDB.category_name == category_name,CategoryDB.category_id != category.category_id)).first()
    if existing_name is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="category name already exists")
    category_model=update_category.model_dump(exclude_unset=True)
    category.sqlmodel_update(category_model)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category
@router.delete("/categories/{category_id}")
def delete_category(session:SessionDep,category_id:int, _=Depends(admin_role)):
    category=session.get(CategoryDB,category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="category not exists")
    session.delete(category)
    session.commit()
    return{"ok":True}
@router.get("/categories/purchases/{category_id}")
def associated_purchases(session:SessionDep,category_id:int,_=Depends(admin_role)):
    category=session.get(CategoryDB,category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="category not exists")
    return category.purchases

    
