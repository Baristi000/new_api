from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException,status,Security
from sqlalchemy.orm import Session

import crud, models, schemas
from crud import crud_shop_sim
from schemas import shop_executor_schema
from api import deps
router = APIRouter()


@router.get("/{shop_id}/all-sim")
def All_shop_executors(
    shop_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["read_shop"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View All shop executors
    '''
    return crud_shop_sim.get_all_shop_sim(db=db,shop_id=shop_id)
