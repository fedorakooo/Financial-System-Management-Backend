from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.main import router

from src.api.startup import app_startup
from src.infrastructure.dependencies.setup import setup_container

container = setup_container()

app = FastAPI()

app.container = container

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", app_startup)

app.include_router(router)
