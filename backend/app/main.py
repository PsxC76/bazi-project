import os
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import init_db
from app.api import users, cases, bazi

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# CORS - 手动中间件，确保生效
@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
    else:
        response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(cases.router, prefix=settings.API_V1_PREFIX)
app.include_router(bazi.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {"message": "八字命理案例库 API", "version": settings.VERSION}

@app.get("/health")
async def health():
    return {"status": "ok"}
