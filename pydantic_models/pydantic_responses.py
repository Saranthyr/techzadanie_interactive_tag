import datetime
from typing import List

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class AccessTokenResponse(BaseModel):
    access_token: str

