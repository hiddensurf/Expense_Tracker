from fastapi import UploadFile,Depends
import csv
from sqlmodel import Session
from app.purchases.models import PurchaseDB
from app.users.models import UserDB
from io import TextIOWrapper
from app.auth.security import get_current_user_active
def parse_csv(csv_file:UploadFile, session:Session,user:UserDB):
    text = TextIOWrapper(csv_file.file,encoding = "utf-8")
    reader = csv.DictReader(text)
    db_purchases=[]
    for row in reader:
        row['user_id'] = user.id
        db_purchases.append(PurchaseDB(**row))
    session.add_all(db_purchases)
    session.flush()
    session.commit()
    return db_purchases
    
        


