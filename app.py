import uuid
from typing import Union
import time
from datetime import timedelta, datetime
from base64 import b64encode

from sqlalchemy import select, exc, update
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Load, selectinload, defaultload, load_only
# from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt
from psycopg import errors

from db import Session
from models import User
# from models import User, Message, File, Foo, FooBar, Bar
# from pydantic_forms import UserCreateForm, UserLoginForm, MessageForm
# from pydantic_responses import ServiceMessageResponse, AccessTokenResponse, UserDataResponse, MessageResponse, \
#     FileResponse
from security import router as security_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(security_router)
