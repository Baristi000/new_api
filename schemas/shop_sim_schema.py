from typing import List, Optional

from pydantic import BaseModel


class Shop_SimBase(BaseModel):
    shop_id:str
    sim_number:str


class  Shop_SimCreate(Shop_SimBase):
    def __init__(self, shop_id, executor_id):
        self.shop_id = shop_id
        self.sim_number = executor_id

    pass

class  Shop_Sim(Shop_SimBase):
    pass

    class Config:
        orm_mode = True