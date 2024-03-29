import datetime as dt
import os
from typing import Optional

import logbook
from fastapi import Depends, APIRouter, Body
from fastapi.params import Security
from fastapi_login import LoginManager
from pydantic import ValidationError
from starlette.responses import Response

from common.mci import MCI_DEPARTMENT
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

WRITE_SCOPE = "write"
ADMIN_SCOPE = "admin"
PLUGIN_SCOPE = "plugin"
REQUIRE_WRITE = Security(login_manager, scopes=[WRITE_SCOPE])
REQUIRE_ADMIN = Security(login_manager, scopes=[ADMIN_SCOPE])
REQUIRE_PLUGIN = Security(login_manager, scopes=[PLUGIN_SCOPE])


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
    current_settings.local_users.register("admin", "admin", is_admin=True)
    current_settings.local_users.register("view", "view", view_only=True)
    current_settings.local_users.register("anon", "anon", anonymous=True)


@auth_router.post("/token")
async def login(
        response: Response,
        s: Settings = Depends(settings),
        auth_provider_name: str = Body(default=None, alias="authProviderName"),
        username=Body(...),
        password=Body(...),
):
    assert auth_provider_name
    user, groups = s.auth.login(provider_name=auth_provider_name, username=username, password=password)
    user.plugin_token = login_manager.create_access_token(
        data=dict(
            # The data in sub (JWT "subject") must conform to whatever load_user(...) expects.
            sub=user.dict()
        ),
        scopes=([PLUGIN_SCOPE]),
        expires=dt.timedelta(hours=8) if not user.view_only else dt.timedelta(days=365)
    )
    access_token = login_manager.create_access_token(
        data=dict(
            # The data in sub (JWT "subject") must conform to whatever load_user(...) expects.
            sub=user.dict()
        ),
        scopes=([ADMIN_SCOPE] if user.is_admin else []) + ([] if user.view_only else [WRITE_SCOPE]),
        expires=dt.timedelta(hours=8) if not user.view_only else dt.timedelta(days=365)
    )

    login_manager.set_cookie(response=response, token=access_token)
    return True


@auth_router.get("/user")
def get_user(user: User = Depends(login_manager), user_settings_=Depends(user_settings)):
    return dict(
        user=dict(
            user=user.username,
            canChangePassword=user.auth_provider_name == "local",
            pluginToken=user.plugin_token,
            is_admin=user.is_admin,
            view_only=user.view_only,
            anonymous=user.anonymous,
        ),
        userSettings=dict(
            theme=getattr(user_settings_, "display", {}).get("theme", "light-theme"),
            statistics=getattr(user_settings_, "statistics", {'default': [
                ('^physician\\.(?!ללא$).*$', False),
                ('^treatment\\.(?!ללא$).*$', False),
                ('^awaiting$', False),
                ('^awaiting\\.doctor$', False),
                ('^awaiting\\.nurse$', False),
                ('^awaiting\\.imaging$', False),
                ('^awaiting\\.referral$', False),
                ('^awaiting\\.laboratory\\..*$', False),
            ]}),
            actions=getattr(user_settings_, "actions", [
                dict(key='new', name='קליטת מטופל', url=f'/views/department/{MCI_DEPARTMENT}/modes/patients#new'),
                dict(key='views', name='צפייה במחלקה', url='/views'),
                dict(key='trauma', name='תצוגה סיכומית', url='/views/custom/trauma/modes/trauma'),
            ])
        ),
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
        raise BadRequestException("New settings are invalid")

    provider = LdapAuthProvider.with_constant_settings(_settings)
    user, groups = provider.login(username=test_user, password=test_password)
    return {"user": user, "groups": groups}


@auth_router.post("/ldap/test_get_user_groups")
async def test_ldap_settings_groups_only(_=REQUIRE_ADMIN, args=Body(...)):
    from ..logics.auth.ldap import LdapSettings, LdapAuthProvider

    test_user = args.pop("test_user")

    try:
        _settings = LdapSettings.create(args)
    except InvalidSettingsException:
        raise BadRequestException("New settings are invalid")

    provider = LdapAuthProvider.with_constant_settings(_settings)
    groups = provider.query_user_groups(username=test_user)
    return {"groups": groups}
