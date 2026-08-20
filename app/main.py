from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.categories.routes import router as category_router
from app.purchases.routes import router as purchase_router
from app import model_registry
app=FastAPI()
app.include_router(auth_router,tags=['Auth'])
app.include_router(users_router,tags=['Users'])
app.include_router(category_router,tags=['Categories'])
app.include_router(purchase_router,tags=['Purchases'])