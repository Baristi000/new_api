from datetime import datetime, timedelta
from typing import  Optional
import random
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi import Depends
from sqlalchemy.orm import Session
from api import deps 
import re
from crud import crud_user
from jose import JWTError, jwt

from passlib.context import CryptContext

from core.config import settings 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_email(email):  
  
    if(re.search(settings.REGEX,email)):  
        return True  
    return False

def check_url(URL):
    if(re.search(settings.URL_REGEX,URL)):  
        return True  
    return False

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


