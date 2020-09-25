from typing import Any, List,Optional
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from fastapi import APIRouter, Depends, HTTPException,status,Header,Security
from sqlalchemy.orm import Session
from core.config import settings
import crud, models, schemas
from crud import crud_channel,crud_shop,crud_channel_manager,crud_user
from schemas import channel_schema
from api import deps
import mysql.connector
router = APIRouter()


@router.get("/")
def all_channel(
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    return crud_channel.get_all_channel_db(db=db)


@router.get("/{channel_id}")
def channel_detail(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):

    return crud_channel.get_channel(db=db,channel_id=channel_id)

@router.get("/{channel_id}/shops")
def channel_detail(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    return crud_shop.get_all_shop_channel(db=db,channel_id=channel_id)


@router.get("/{channel_id}/shop-count")
def Count_shop_of_channel(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    return crud_shop.count_shop(db=db,channel_id=channel_id)

@router.get("/{channel_id}/manager-count")
def Number_of_channel_manager(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    return crud_channel_manager.count_manager_of_channel(db=db,channel_id=channel_id)

@router.get("/{channel_id}/all-manager")
def all_channel_manager(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    return crud_user.get_all_channel_manager(db=db,channel_id=channel_id)

@router.get("/{channel_id}/all-manager-not_channel")
def all_channel_manager_not_belong_to_channel(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    return crud_user.get_all_manager_not_belong_to_channel(db=db,channel_id=channel_id)

@router.post("/{channel_id}/add-manager")
def add_manager_from_channel(
    channel_id:str,
    managers_id:List[str],
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    if len(managers_id) ==0:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid manager id list "
        )
    for id in managers_id:
        if crud_user.get_user(db=db,user_id=id) is None or crud_user.get_user(db=db,user_id=id).role!="manager":
            raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid manager id list "
        )
    for id in managers_id:
        if not crud_channel_manager.get_channel_manager(db=db,channel_id=channel_id,manager_id=id) is None:
            raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Manager already asign to channel"
        )
    for id in managers_id:
        crud_channel_manager.create_channel_manager(db=db,manager_id=id,channel_id=channel_id)
    return {"message":"add success"}

@router.post("/{channel_id}/deltete-manager")
def delete_manager_from_channel(
    channel_id:str,
    managers_id:List[str],
    current_user= Security(deps.get_current_active_user,scopes=["read_channel"]),
    db: Session = Depends(deps.get_db)
):
    if len(managers_id) ==0:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid manager id list "
        )
    for id in managers_id:
        if crud_user.get_user(db=db,user_id=id) is None or crud_user.get_user(db=db,user_id=id).role!="manager":
            raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid manager id list "
        )
    for id in managers_id:
        if crud_channel_manager.get_channel_manager(db=db,channel_id=channel_id,manager_id=id) is None:
            raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Manager not asign to channel"
        )
    for id in managers_id:
        crud_channel_manager.delete_channel_manager(db=db,manager_id=id,channel_id=channel_id)
    return {"message":"update success"}

    