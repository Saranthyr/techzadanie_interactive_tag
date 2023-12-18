import time
from datetime import datetime, timedelta
from base64 import b64encode
from typing import Union

from fastapi import APIRouter, Response, Depends
from sqlalchemy import select
from jose import jwt
from cryptography.fernet import Fernet

from config import oauth2_scheme
from db import Session
from models import User
from pydantic_models.pydantic_forms import UserLoginForm
from pydantic_models.pydantic_responses import MessageResponse, AccessTokenResponse

router = APIRouter(prefix="/auth")

f = Fernet(b'8qaCL_hUezsq7g_ZpJLO2KdHnAI090-qTBVNBVuJRgA=')
secret = b'A\xa3\x8c\x9a>\x96\xd6njF\x8a%j\x9bil\xfe\x8aq\xd6\xe8\x87\xfe:\xea\xf7\x18q\xc3\xaeK\x88\xe0\x91\xae\x85\
xcd\xcf\xd0q:\xb1\xf3\xb5\x16\x164\xe3"/\x10_\xb5\xff\x8c\xae\x85\x86\xc8\xdbI)\x98['
secret = b64encode(secret)


@router.post('/login')
def login_post(response: Response,
               formdata: UserLoginForm = Depends(UserLoginForm.as_form)):
    session = Session()

    try:
        uid = session.execute(select(User.id).
                              where(User.username == formdata.username)).scalar_one_or_none()
        assert uid is not None
        user = session.get(User, uid)
        assert user.compare_hash(formdata.password) is True
        access_token = jwt.encode({'id': str(uid),
                                   'iat': time.time(),
                                   'exp': (datetime.fromtimestamp(time.time()) + timedelta(hours=1)).timestamp(),
                                   'nbf': (datetime.fromtimestamp(time.time()) + timedelta(milliseconds=10)).
                                  timestamp()},
                                  str(secret),
                                  algorithm='HS384')
        access_token = b64encode(f.encrypt(bytes(access_token, encoding='utf-8'))).decode('utf-8')
        response.set_cookie('Authorization', f'Bearer {access_token}')
        return AccessTokenResponse(access_token=access_token)
    except AssertionError:
        response.status_code = 403
        return MessageResponse(message='Incorrect credentials')


@router.post('/logout',
             response_model=MessageResponse)
def logout_post(response: Response,
                token: Union[str, dict] = Depends(oauth2_scheme)):
    response.delete_cookie('Authorization')
    return MessageResponse(message='Successfully logged out')
