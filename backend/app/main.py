from fastapi import FastAPI

from app import models
from app.api.main import api_router
from app.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
API_version_string = "/api/v1/"
