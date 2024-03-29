from typing import List, Optional, AnyStr

from pydantic import BaseModel
from fastapi import Form


class UserRegisterForm(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    dealer: int

    @classmethod
    def as_form(cls,
                username: str = Form(...),
                password: str = Form(...),
                first_name: str = Form(...),
                last_name: str = Form(...),
                dealer: int = Form(...),
                ):
        return cls(username=username,
                   password=password,
                   first_name=first_name,
                   last_name=last_name,
                   dealer=dealer)


class UserLoginForm(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls,
                username: str = Form(...),
                password: str = Form(...)):
        return cls(
            username=username,
            password=password
        )
