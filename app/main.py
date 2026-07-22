from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app import model_registry
app=FastAPI()
app.include_router(auth_router,tags=['Auth'])