import interruptingcow
import logbook
from contextlib import asynccontextmanager
from fastapi import Depends, APIRouter, Body
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.responses import Response
import ldap


SECRET = 'asdfsfgdfgsherfdbfsr'

auth_router = APIRouter()
manager = LoginManager(SECRET, token_url='/auth/token', use_cookie=True)

logger = logbook.Logger(__name__)


@manager.user_loader()
async def load_user(username: str):
    return {'username': username, 'password': 'admin'}


@auth_router.post('/token')
async def login(response: Response, username=Body(...), password=Body(...)):
    user = await load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    manager.set_cookie(response, access_token)
    return True


@auth_router.post('/change-password')
async def change_password(user=Depends(manager), previous=Body(...), password=Body(...), confirm=Body(...)):
    return True


@auth_router.get('/ldap')
async def get_ldap_settings(user=Depends(manager)):
    return dict(
        connection='ldap://ldap.forumsys.com',
        bind_dn='cn=read-only-admin,dc=example,dc=com',
        bind_password='password',
        admin_ou='ou=mathematicians,dc=example,dc=com',
        users_ou='ou=scientists,dc=example,dc=com',
        test_user='einstein',
        test_password='password',
    )


@auth_router.post('/ldap')
async def update_ldap_settings(user=Depends(manager), previous=Body(...), password=Body(...), confirm=Body(...)):
    return True


@auth_router.post('/ldap/test')
async def test_ldap_settings(args=Body(...), user=Depends(manager)):
    try:
        with interruptingcow.timeout(seconds=1, exception=TimeoutError):
            connection = ldap.initialize(args['connection'])
            connection.whoami_s()
            return True
    except (ldap.SERVER_DOWN, TimeoutError) as e:
        return False


@auth_router.get('/user')
def get_user(user=Depends(manager)):
    return dict(user='foo', canChangePassword=True, admin=True)
