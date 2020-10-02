from typing import Any, List,Optional
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException,status,Header,Security
from sqlalchemy.orm import Session
import json
import crud, models, schemas
from crud import crud_user,crud_shop,crud_channel,crud_shop_executor,crud_channel_manager,crud_url,crud_sim_url,crud_sim
from schemas import user_schema,shop_schema,channel_schema,url_schema
from api import deps
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from core import sercurity
import mysql.connector
router = APIRouter()

@router.get("/",tags=["url"])
def all_url(
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View all url
    '''
    return crud_url.get_all_url(db=db)


@router.post("/add-new-url",tags=["url"])
def add_new_url(
    new_url:url_schema.URLCreate,
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Create new URL
    '''
    if sercurity.check_url(URL=new_url.url) is False:
        raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Wrong URL "
            )
    return crud_url.create_new_url(db=db,new_url=new_url.url)

@router.post("/update-url",tags=["url"])
def update_url(
    url_id:str,
    new_url:str,
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Update URL
    '''
    if crud_url.get_url(db=db,id=url_id) is None:
        raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Url not found"
            )
    crud_url.update_url(db=db,id=url_id,new_url=new_url)
    return {"message":" success"}


@router.post("/asign-url-to-sim",tags=["url"])
def asign_url_to_sim(
    sim:List[str],
    url:List[str],
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Asign url to sim 
    '''
    for s in sim:
        if crud_sim.get_sim_by_number(db=db,sim_number=s) is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Sim not found"
            )
    for u in url:
        if crud_url.get_url(db=db,id=u) is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Url not found"
            )
    for s in sim:
        for u in url:
            if not crud_sim_url.get_sim_url(db=db,sim_number=s,url_id=u) is None:
                raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Sim url already exist"
            )
    for s in sim:
        for u in url:
            crud_sim_url.create_new_sim_url(db=db,sim_number=s,url_id=u)
            
    return {"message":" success"}



