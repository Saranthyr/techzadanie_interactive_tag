import uuid

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, or_, and_

from db import Session
from db.models import User, Dealer, DealerUser
from pydantic_models.pydantic_forms import UserRegisterForm
from pydantic_models.pydantic_responses import MessageResponse

router = APIRouter(prefix="/registration")


@router.post('/',
             responses={
                 200: MessageResponse.model_json_schema(),
                 409: MessageResponse.model_json_schema()
             })
def register_post(response: Response,
                  formdata: UserRegisterForm = Depends(UserRegisterForm.as_form)):
    session = Session()

    try:
        assert session.execute(select(User.username,
                                      User.first_name,
                                      User.last_name,
                                      User.middle_name).where(or_(User.username == formdata.username,
                                                                  and_
                                                                  (User.first_name == formdata.first_name,
                                                                   User.last_name == formdata.last_name,
                                                                   User.middle_name == formdata.middle_name)))).\
                   one_or_none() is None

    except AssertionError:
        response.status_code = 409
        return MessageResponse(message='User with such credentials is already in system')

    try:
        assert session.execute(select(Dealer.name).
                               where(Dealer.id == formdata.dealer)).scalar_one_or_none() is not None
    except AssertionError:
        response.status_code = 404
        return MessageResponse(message='No such dealer found')

    try:
        assert session.execute(select(DealerUser.user_id).
                               where(DealerUser.dealer_id == formdata.dealer)).scalar_one_or_none() is None
    except AssertionError:
        response.status_code = 409
        return MessageResponse(message='This dealer already has designated user')

    uid = uuid.uuid4()
    user = User(
        id=uid,
        username=formdata.username,
        first_name=formdata.first_name,
        last_name=formdata.last_name,
        middle_name=formdata.middle_name,
        password=formdata.password
    )
    user.generate_salted_hash()
    session.add(user)
    session.commit()
    session.close()
    response.status_code = 200
    return MessageResponse(message='Success')

