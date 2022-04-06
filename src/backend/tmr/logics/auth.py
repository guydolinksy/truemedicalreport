from fastapi import Depends, APIRouter, Body
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import Response

SECRET = 'asdfsfgdfgsherfdbfsr'

auth_router = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token', use_cookie=True)


@manager.user_loader()
def load_user(username: str):  # could also be an asynchronous function
    return {'username': username, 'password': 'admin'}


@auth_router.post('/token')
def login(response: Response, username=Body(...), password=Body(...)):
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    manager.set_cookie(response, access_token)
    return True
