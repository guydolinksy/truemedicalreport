import os

import interruptingcow
import ldap
import logbook
from fastapi import Depends, APIRouter, Body
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import Response
from .settings import Settings, settings, current_settings, LDAP

logger = logbook.Logger(__name__)
auth_router = APIRouter()


def init_manager():
    if not hasattr(current_settings.general, 'secret'):
        current_settings.general.secret = os.urandom(256).hex()
    res = LoginManager(current_settings.general.secret, token_url='/auth/token', use_cookie=True)

    @res.user_loader()
    async def load_user(sub: str):
        user_type, username = sub.split('#')
        return {'username': username, 'source': user_type}

    return res


manager = init_manager()


@auth_router.on_event('startup')
def init_auths():
    if not current_settings.users['admin']:
        current_settings.users['admin'] = 'admin'


@auth_router.post('/token')
async def login(response: Response, s: Settings = Depends(settings), username=Body(...), password=Body(...)):
    user_type = s.auth.connect(username, password)
    access_token = manager.create_access_token(
        data=dict(sub='#'.join([user_type, username]))
    )
    manager.set_cookie(response, access_token)
    return True


@auth_router.post('/change-password')
async def change_password(user=Depends(manager), s: Settings = Depends(settings), previous=Body(...),
                          password=Body(...), confirm=Body(...)):
    if password != confirm or (user['username'], previous) not in s.users:
        raise InvalidCredentialsException

    s.users[user['username']] = password
    return True


@auth_router.get('/ldap')
async def get_ldap_settings(_=Depends(manager), s: Settings = Depends(settings)) -> LDAP:
    return s.ldap.settings


@auth_router.post('/ldap')
async def update_ldap_settings(_=Depends(manager), s: Settings = Depends(settings), values=Body(...)):
    s.ldap.settings = values


@auth_router.post('/ldap/test')
async def test_ldap_settings(_=Depends(manager), args=Body(...)):
    try:
        with interruptingcow.timeout(seconds=1, exception=TimeoutError):
            connection = ldap.initialize(args['connection'])
            connection.whoami_s()
            return True
    except (ldap.SERVER_DOWN, TimeoutError):
        return False


@auth_router.get('/user')
def get_user(user=Depends(manager)):
    return dict(user=user['username'], canChangePassword=user['source'] == 'local', admin=user['source'] == 'local')
