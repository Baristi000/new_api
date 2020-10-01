from typing import List, Optional

from pydantic import BaseModel


class SimBase(BaseModel):
    sim_number:Optional[str] = None


class SimCreate(SimBase):
    port_number: str
    tty_gateway: str
    status:str


class Sim(SimBase):
    tty_gateway:Optional[str] = None
    status:Optional[str] = None

    class Config:
        orm_mode = True