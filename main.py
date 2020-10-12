from typing import List
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Request, Response,status
from sqlalchemy.orm import Session
from models import user,token
from db.database import SessionLocal, engine
from api.api_v1.api import api_router
from api import deps
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from core.config import settings
import crud
from core import sercurity
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from schemas import exception
from fastapi.responses import JSONResponse
import mysql.connector
user.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
@app.exception_handler(exception.UnicornException)
async def unicorn_exception_handler(request: Request, exc: exception.UnicornException):
    return JSONResponse(
        status_code=502,
        content={"message": f"{exc.messages}: {exc.name}"}
    )


app.include_router(api_router)