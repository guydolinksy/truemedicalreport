import os

import ldap
import logbook
from fastapi import Depends, APIRouter, Body
from fastapi_login import LoginManager
from starlette.responses import Response

from ..logics.exceptions import UnauthorizedException
from ..logics.settings import Settings, settings, current_general_settings, Proxy, current_settings
from ..logics.user import User
from ..logics.ldap_auth import LdapAuth

logger = logbook.Logger(__name__)
auth_router = APIRouter()


def get_login_manager():
    if not hasattr(current_general_settings, 'secret'):
        current_general_settings.secret = os.urandom(256).hex()

    _manager = LoginManager(current_general_settings.secret, token_url='/auth/token', use_cookie=True)

    @_manager.user_loader()
    async def load_user(sub: dict) -> User:
        return User(**sub)

    return _manager


login_manager = get_login_manager()


def user_settings(user: User = Depends(login_manager), settings_=Depends(settings)) -> Proxy:
    return settings_.for_user(user.username)


@auth_router.on_event('startup')
def init_auths():
    if not current_settings.local_users.has_user('admin'):
        current_settings.local_users.register("admin", "admin")


@auth_router.post('/token')
async def login(response: Response, s: Settings = Depends(settings), username=Body(...), password=Body(...)):
    user = s.auth.login(username, password)
    access_token = login_manager.create_access_token(
        data=dict(sub=user.dict())
    )
    login_manager.set_cookie(response, access_token)
    return True


@auth_router.post('/change-password')
async def change_password(
        user: User = Depends(login_manager),
        s: Settings = Depends(settings),
        previous=Body(...),
        password=Body(...),
        confirm=Body(...)
):
    if password != confirm:
        raise UnauthorizedException("The confirmation password does not match")

    if user.source != "local":
        raise UnauthorizedException(f"User `{user.username}` is not a local user")

    if not s.local_users.login(user.username, previous):
        raise UnauthorizedException("Incorrect password")

    s.local_users.register(user.username, password)
    return True


@auth_router.get('/ldap')
async def get_ldap_settings(_=Depends(login_manager), s: Settings = Depends(settings)) -> LdapAuth:
    return s.ldap.settings


@auth_router.post('/ldap')
async def update_ldap_settings(_=Depends(login_manager), s: Settings = Depends(settings), values=Body(...)):
    s.ldap.update_settings(values)


@auth_router.post('/ldap/test')
async def test_ldap_settings(_=Depends(login_manager), args=Body(...)):
    try:
        test_user = args.pop("test_user")
        test_password = args.pop("test_password")

        return LdapAuth(**args).auth_with_groups(
            login_source="ldap",
            username=test_user,
            password=test_password
        )
    except (ldap.SERVER_DOWN, TimeoutError):
        raise UnauthorizedException("Failed to reach the ldap server")


@auth_router.post('/ldap/test_get_user_groups')
async def test_ldap_settings_groups_only(_=Depends(login_manager), args=Body(...)):
    try:
        test_user = args.pop("test_user")
        return {
            "groups": LdapAuth(**args).query_user_groups(username=test_user)
        }
    except (ldap.SERVER_DOWN, TimeoutError):
        raise UnauthorizedException("Failed to reach the ldap server")


@auth_router.get('/user')
def get_user(user: User = Depends(login_manager), user_settings_=Depends(user_settings)):
    return dict(
        user=dict(
            user=user.username,
            canChangePassword=user.source == 'local',
            admin=user.is_admin,
            groups=user.groups,
        ),
        userSettings=dict(
            theme=getattr(user_settings_, 'display', {}).get('theme', 'light-theme')
        )
    )
