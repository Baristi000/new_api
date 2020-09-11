from typing import List, Optional

from pydantic import BaseModel


class SimBase(BaseModel):
    sim_number:str


class SimCreate(SimBase):
    port_number: str
    tty_gateway: str
    status:str

class Sim(SimBase):
    port_number: str
    tty_gateway: str
    status:str

    class Config:
        orm_mode = True