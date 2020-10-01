from typing import Any, List,Optional
from fastapi import APIRouter, Depends, HTTPException,Header,status,Security
from sqlalchemy.orm import Session
from core.config import settings
import crud, models, schemas
from crud import crud_sim,crud_message,crud_shop_sim,crud_shop
from schemas import sim_schema,message_schema
from api import deps
router = APIRouter()


@router.get("/")
def get_all_sim(
    current_user= Security(deps.get_current_active_user,scopes=["read_sim"]),
    db: Session = Depends(deps.get_db)
):
    return crud_sim.get_all_sim(db=db)


@router.get("/{sim_number}")
def sim_details(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_sim"]),
    db: Session = Depends(deps.get_db)
):
    return crud_sim.get_sim_by_number(db=db,sim_number=sim_number)

@router.get("/{sim_number}/shops")
def sim_details(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_sim"]),
    db: Session = Depends(deps.get_db)
):
    return crud_shop.get_all_shop_of_sim(db=db,sim_number=sim_number)

@router.get("/{sim_number}/all-messages")
def all_sim_message(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_sim"]),
    db: Session = Depends(deps.get_db)
):
    return crud_sim.get_message(db=db,sim_number=sim_number)

@router.get("/{sim_number}/shop-count")
def get_sim_db(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_sim"]),
    db: Session = Depends(deps.get_db)
):
    return crud_sim.count_shop(db=db,sim_number=sim_number)








