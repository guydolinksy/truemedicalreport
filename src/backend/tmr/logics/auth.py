import shelve

import interruptingcow
import logbook
from contextlib import asynccontextmanager
from fastapi import Depends, APIRouter, Body
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import Response
import ldap

from tmr.logics.settings import settings

logger = logbook.Logger(__name__)
auth_router = APIRouter()

manager = LoginManager(settings.secret, token_url='/auth/token', use_cookie=True)


@manager.user_loader()
async def load_user(sub: str):
    user_type, username = sub.split('#')
    return {'username': username, 'source': user_type}


@auth_router.post('/token')
async def login(response: Response, username=Body(...), password=Body(...)):
    if local_connect(username, password):
        user_type = 'local'
    elif ldap_connect(username, password):
        user_type = 'ldap'
    else:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub='#'.join([user_type, username]))
    )
    manager.set_cookie(response, access_token)
    return True


@auth_router.post('/change-password')
async def change_password(user=Depends(manager), previous=Body(...), password=Body(...), confirm=Body(...)):
    username = user['username']
    users = {user: password for user, password in (settings.users or {}).items()}
    if username not in users or users[username] != previous or password != confirm:
        raise InvalidCredentialsException

    users[username] = password
    settings.users = users
    return True


@auth_router.get('/ldap')
async def get_ldap_settings(user=Depends(manager)):
    return settings.ldap


def ldap_connect(username, password):
    ldap_settings = settings.ldap or {}
    logger.debug(ldap_settings)
    if not ldap_settings.get('enabled'):
        return False

    with interruptingcow.timeout(seconds=5, exception=TimeoutError):
        connection = ldap.initialize(ldap_settings['connection'])
        return connection.bind_s(ldap_settings.get('user_dn', '{}').format(username), password)


def local_connect(username, password):
    users = settings.users or {}
    if username in users:
        return users[username] == password


@auth_router.post('/ldap')
async def update_ldap_settings(user=Depends(manager), values=Body(...)):
    settings.ldap = values


@auth_router.post('/ldap/test')
async def test_ldap_settings(user=Depends(manager), args=Body(...)):
    try:
        with interruptingcow.timeout(seconds=1, exception=TimeoutError):
            connection = ldap.initialize(args['connection'])
            connection.whoami_s()
            return True
    except (ldap.SERVER_DOWN, TimeoutError) as e:
        return False


@auth_router.get('/user')
def get_user(user=Depends(manager)):
    return dict(user=user['username'], canChangePassword=user['source'] == 'local', admin=user['source'] == 'local')
