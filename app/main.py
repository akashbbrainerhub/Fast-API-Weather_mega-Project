from fastapi import FastAPI
from app.api.V1.dependencies.auth import router as auth_router
from app.core.middleware import LoggingMiddleware
from app.api.V1.routes import weather
from app.db.base_class import Base
from app.api.V1.routes import saved_city
from app.api.V1.routes import admin
from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI()
app.add_middleware(LoggingMiddleware)

app.include_router(auth_router)
app.include_router(weather.router)
app.include_router(saved_city.router)
app.include_router(admin.router)
from app.api.V1.routes import analytics

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )
app.include_router(analytics.router)