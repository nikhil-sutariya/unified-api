from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from startup import startup
from app.routers import user_router
settings = get_settings()

app = FastAPI()
app = FastAPI(title=settings.app_title, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.client_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_event_handler("startup", startup)
app.include_router(user_router, tags=['Users'], prefix='/api/v1/users')


@app.get("/")
def root():
    return {"message": "Welcome to Unified API"}
