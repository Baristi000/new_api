from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List
import crud, models, schemas
from crud import crud_country
from schemas import country_schema
from api import deps
router = APIRouter()



@router.post("/", response_model=List[country_schema.Country])
def View_all_Countries(db: Session = Depends(deps.get_db)):
    return crud_country.get_all_country(db=db)

@router.get("/{country_id}", response_model=country_schema.Country)
def View_country_detail(postal_code:str, db: Session = Depends(deps.get_db)):
    return crud_country.get_country(db=db,country_id=postal_code)

    