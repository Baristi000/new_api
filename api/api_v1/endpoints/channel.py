from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from crud import crud_channel,crud_shop,crud_channel_manager,crud_user
from schemas import channel_schema
from api import deps
router = APIRouter()



@router.get("/{id}", response_model=channel_schema.Channel)
def get_channel_db(id:str, db: Session = Depends(deps.get_db)):
    return crud_channel.get_channel(db=db,channel_id=id)

@router.get("/{channel_id}/shop-count")
def Count_shop_of_channel(channel_id:str, db: Session = Depends(deps.get_db)):
    return crud_shop.count_shop(db=db,channel_id=channel_id)

@router.get("/{channel_id}/manager-count")
def Count_manager_of_channel(channel_id:str, db: Session = Depends(deps.get_db)):
    return crud_channel_manager.count_manager_of_channel(db=db,channel_id=channel_id)

@router.get("/{channel_id}/all-manager")
def all_channel_manager(channel_id:str, db: Session = Depends(deps.get_db)):
    return crud_user.get_all_channel_manager(db=db,channel_id=channel_id)

@router.get("/{channel_id}/all-manager-not_channel")
def all_channel_manager_not_belong_to_channel(channel_id:str, db: Session = Depends(deps.get_db)):
    return crud_user.get_all_manager_not_belong_to_channel(db=db,channel_id=channel_id)

@router.post("/", response_model=List[channel_schema.Channel])
def all_channel(db: Session = Depends(deps.get_db)):
    return crud_channel.get_all_channel(db=db)


    