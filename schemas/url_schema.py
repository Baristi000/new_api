from typing import List, Optional

from pydantic import BaseModel


class UrlBase(BaseModel):
    url:Optional[str] = None
    value:Optional[str] = None


class URLCreate(UrlBase):
    pass

