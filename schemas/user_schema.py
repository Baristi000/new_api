from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    role: str

class User(UserBase):
    id: str
    role:Optional[str] = None
    activate:Optional[str] = None
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    last_login:Optional[str] = None

    class Config:
        orm_mode = True