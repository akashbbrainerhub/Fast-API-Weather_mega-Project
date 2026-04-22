from fastapi import FastAPI
from app.api.V1.dependencies.auth import router as auth_router
from app.core.middleware import LoggingMiddleware
from app.api.V1.routes import weather
from app.db.base_class import Base
from app.api.V1.routes import saved_city

app = FastAPI()
app.include_router(auth_router)
app.add_middleware(LoggingMiddleware)

app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(saved_city.router)