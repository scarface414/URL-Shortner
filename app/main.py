from fastapi import FastAPI
from .url_routes import router

app = FastAPI() 
app.include_router(router)
