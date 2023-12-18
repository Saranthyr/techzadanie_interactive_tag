from typing import List, Optional, AnyStr

from pydantic import BaseModel
from fastapi import Form


class UserRegisterForm(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    middle_name: Optional[str]

    @classmethod
    def as_form(cls,
                username: str = Form(...),
                password: str = Form(...),
                first_name: str = Form(...),
                last_name: str = Form(...),
                middle_name: Optional[str] = Form(None),
                ):
        return cls(username=username,
                   password=password,
                   first_name=first_name,
                   last_name=last_name,
                   middle_name=middle_name)


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