import os
from typing import Optional

import logbook
from fastapi import Depends, APIRouter, Body
from fastapi.params import Security
from fastapi_login import LoginManager
from pydantic import ValidationError
from starlette.responses import Response
import datetime as dt

from .. import config
from ..logics.exceptions import UnauthorizedException, InvalidSettingsException, BadRequestException
from ..logics.settings import Settings, settings, current_general_settings, Proxy, current_settings
from ..logics.user import User


logger = logbook.Logger(__name__)
auth_router = APIRouter()


def _create_login_manager() -> LoginManager:
    if not hasattr(current_general_settings, "secret"):
        current_general_settings.secret = os.urandom(256).hex()

    return LoginManager(current_general_settings.secret, token_url="/auth/token", use_cookie=True)


login_manager = _create_login_manager()

ADMIN_SCOPE = "admin"
REQUIRE_ADMIN = Security(login_manager, scopes=[ADMIN_SCOPE])


@login_manager.user_loader()
async def load_user(sub: dict) -> Optional[User]:
    try:
        return User(**sub)
    except (TypeError, ValidationError):
        # Invalid object, probably stale data on the client side.
        # Forcing re-login.
        return None


def user_settings(user: User = Depends(login_manager), settings_: Settings = Depends(settings)) -> Proxy:
    return settings_.for_user(user.username)


@auth_router.on_event("startup")
def init_auths():
    current_settings.local_users.register("admin", "admin")


@auth_router.post("/token")
async def login(
    response: Response,
    s: Settings = Depends(settings),
    auth_provider_name: str = Body(default=None, alias="authProviderName"),
    username=Body(...),
    password=Body(...),
):
    assert auth_provider_name
    user = s.auth.login(provider_name=auth_provider_name, username=username, password=password)
    access_token = login_manager.create_access_token(
        data=dict(
            # The data in sub (JWT "subject") must conform to whatever load_user(...) expects.
            sub=user.dict()
        ),
        scopes=([ADMIN_SCOPE] if user.is_admin else []),
        expires=dt.timedelta(hours=12)
    )
    login_manager.set_cookie(response, access_token)
    return True


@auth_router.get("/user")
def get_user(user: User = Depends(login_manager), user_settings_=Depends(user_settings)):
    return dict(
        user=dict(
            user=user.username,
            canChangePassword=user.auth_provider_name == "local",
            admin=user.is_admin,
            groups=user.groups,
        ),
        userSettings=dict(theme=getattr(user_settings_, "display", {}).get("theme", "light-theme")),
    )


@auth_router.post("/change-password")
async def change_password(
    user: User = Depends(login_manager),
    s: Settings = Depends(settings),
    previous=Body(...),
    password=Body(...),
    confirm=Body(...),
):
    if password != confirm:
        raise UnauthorizedException("The confirmation password does not match")

    s.local_users.login(user.username, previous)
    s.local_users.register(user.username, password)
    return True


@auth_router.get("/ldap-status")
async def get_ldap_status(s: Settings = Depends(settings)) -> dict:
    return {
        "enabled": config.LDAP_SUPPORTED and s.ldap.is_enabled(),
        "supported": config.LDAP_SUPPORTED,
    }


@auth_router.get("/ldap")
async def get_ldap_settings(_=REQUIRE_ADMIN, s: Settings = Depends(settings)) -> dict:
    return s.ldap.settings.raw


@auth_router.post("/ldap")
async def update_ldap_settings(_=REQUIRE_ADMIN, s: Settings = Depends(settings), values=Body(...)):
    s.ldap.update_settings(values)


@auth_router.post("/ldap/test")
async def test_ldap_settings(_=REQUIRE_ADMIN, args=Body(...)):
    from ..logics.auth.ldap import LdapSettings, LdapAuthProvider

    test_user = args.pop("test_user")
    test_password = args.pop("test_password")

    try:
        _settings = LdapSettings.create(args)
    except InvalidSettingsException:
        raise BadRequestException("New setting are invalid")

    provider = LdapAuthProvider.with_constant_settings(_settings)
    return provider.login(username=test_user, password=test_password)


@auth_router.post("/ldap/test_get_user_groups")
async def test_ldap_settings_groups_only(_=REQUIRE_ADMIN, args=Body(...)):
    from ..logics.auth.ldap import LdapSettings, LdapAuthProvider

    test_user = args.pop("test_user")

    try:
        _settings = LdapSettings.create(args)
    except InvalidSettingsException:
        raise BadRequestException("New setting are invalid")

    provider = LdapAuthProvider.with_constant_settings(_settings)
    groups = provider.query_user_groups(username=test_user)
    return {"groups": groups}
