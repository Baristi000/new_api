from typing import Any, List,Optional

from fastapi import APIRouter, Depends, HTTPException,Header,status,Security
from sqlalchemy.orm import Session

from typing import List
import crud, models, schemas
from crud import crud_country,crud_shop
from schemas import country_schema
from api import deps
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
import mysql.connector
from schemas.exception import UnicornException
router = APIRouter()



@router.post("/")
def View_all_Countries(
    current_user= Security(deps.get_current_active_user,scopes=["read_country"]),
    db: Session = Depends(deps.get_db)
):
    return crud_country.get_all_country(db=db)

@router.get("/{postal_code}", response_model=country_schema.Country)
def View_country_detail(
    postal_code:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_country"]),
    db: Session = Depends(deps.get_db)
):
    if crud_country.get_country(db=db,country_id=postal_code) is None:
        raise UnicornException(
            messages="COUNTRY ID NOT FOUND",
            name=postal_code
            )
    return crud_country.get_country(db=db,country_id=postal_code)

@router.get("/{postal_code}/all_shop")
def View_country_detail(
    postal_code:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_country"]),
    db: Session = Depends(deps.get_db)
):
    if crud_country.get_country(db=db,country_id=postal_code) is None:
        raise UnicornException(
            messages="COUNTRY ID NOT FOUND",
            name=postal_code
            )
    return crud_shop.get_all_shop_country(db=db,postal_code=postal_code)

    