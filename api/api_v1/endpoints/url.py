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
from schemas.exception import UnicornException
router = APIRouter()

@router.get("/")
def all_url(
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View all url
    '''
    return crud_url.get_all_url(db=db)


@router.post("/add-new-url")
def add_new_url(
    url_list:List[str],
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Create new URL
    '''
    url_fail_list=[]

    for url in url_list:
        if sercurity.check_url(url) is None:
            url_fail_list.append(url)

    if len(url_fail_list) !=0:
        raise UnicornException(
            messages="Wrong URL format",
            name=url_fail_list
            )

    for url in url_list:
        crud_url.create_new_url(db=db,new_url=url)
    return url_list

@router.post("/delete-url")
def Delete_url_list(
    id_list:List[str],
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Create new URL
    '''
    invalid_list=[]
    for id in id_list:
        if crud_url.get_url(db=db,id=id) is None:
            invalid_list.append(id)
    
    if len(invalid_list) !=0:
        raise UnicornException(
            messages="URL ID NOT FOUNT",
            name=invalid_list
        )
    for url in id_list:
        crud_url.delete_url(db=db,id=url)
    return id_list

@router.post("/update-url")
def update_url(
    url_id:str,
    new_url:str,
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Update URL
    '''
    if sercurity.check_email(new_url) is None:
        raise UnicornException(
            messages="INVALID URL FORMAT",
            name=new_url
            )
    if crud_url.get_url(db=db,id=url_id) is None:
        raise UnicornException(
                messages="URL Not Found",
                name=url_id
            )
    crud_url.update_url(db=db,id=url_id,new_url=new_url)
    return {"message":" success"}

@router.get("/all-url-sim")
def View_all_URL_of_sim(
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View all url
    '''
    return crud_sim_url.get_all_sim_url(db=db)


@router.post("/asign-url-to-sim")
def asign_url_to_sim(
    sim:List[str],
    url:List[str],
    current_user= Security(deps.get_current_active_user,scopes=["url"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Asign url to sim 
    '''
    invalid_list=[]
    for s in sim:
        if crud_sim.get_sim_by_number(db=db,sim_number=s) is None:
            invalid_list.append(s)
    if len(invalid_list) !=0:
        raise UnicornException(
                messages="SIM NUMBER NOT FOUND",
                name=invalid_list
            )
    for u in url:
        if crud_url.get_url(db=db,id=u) is None:
            invalid_list.append(u)
    
    if len(invalid_list) !=0:
        raise UnicornException(
                messages="URL ID NOT FOUND",
                name=invalid_list
                )
    for s in sim:
        for u in url:
            if not crud_sim_url.get_sim_url(db=db,sim_number=s,url_id=u) is None:
                invalid_list.append([s,u])
    
    if len(invalid_list) !=0:
        raise UnicornException(
                messages="URL&SIM ALREADY ASIGN",
                name=invalid_list
                )
    for s in sim:
        for u in url:
            crud_sim_url.create_new_sim_url(db=db,sim_number=s,url_id=u)
            
    return {"message":" success"}



