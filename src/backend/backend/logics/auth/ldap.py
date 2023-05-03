import contextlib
from typing import Tuple, Set, List, Any, Dict

import ldap
import logbook
import pydantic.dataclasses
from cachetools import cached, TTLCache
from ldap.ldapobject import LDAPObject
from pydantic import ValidationError
from pymongo.collection import Collection

from .base import AuthProvider
from ..exceptions import UnauthorizedException, InvalidSettingsException, ForbiddenException
from ..user import User

LDAP_MEMBER_IN_GROUP_ATTRIBUTE = "memberOf"

# See https://ldapwiki.com/wiki/Active%20Directory%20User%20Related%20Searches#section-Active+Directory+User+Related+Searches-AllGroupsAUserIsAMemberOfIncludingNestedGroups
LDAP_MATCHING_RULE_IN_CHAIN = "1.2.840.113556.1.4.1941"

logger = logbook.Logger("ldap-provider")


class LdapSettingsLoader:
    def get(self) -> "LdapSettings":
        raise NotImplementedError()

    def set(self, new_settings: dict) -> None:
        raise NotImplementedError()


class MongoLdapSettingsLoader(LdapSettingsLoader):
    def __init__(self, collection: Collection, key: str) -> None:
        self.collection = collection
        self.key = key

    @cached(cache=TTLCache(maxsize=1, ttl=30))  # Reloads every 30 seconds
    def get(self) -> "LdapSettings":
        if res := self.collection.find_one({"type": self.key}):
            del res["_id"]
            del res["type"]
            return LdapSettings.create_or_disable(res)

        return LdapSettings.create_disabled()

    def set(self, new_settings: dict) -> None:
        LdapSettings.create(new_settings)
        self.collection.replace_one({"type": self.key}, {"type": self.key, **new_settings}, upsert=True)
        self.get.cache_clear()


class ConstantLdapSettingsLoader(LdapSettingsLoader):
    def __init__(self, settings: "LdapSettings") -> None:
        self._settings = settings

    def get(self) -> "LdapSettings":
        return self._settings

    def set(self, new_settings: dict) -> None:
        raise Exception("Settings are constant")


class LdapAuthProvider(AuthProvider):
    name = "ldap"

    def __init__(self, settings_loader: LdapSettingsLoader) -> None:
        self._settings_loader = settings_loader

    @staticmethod
    def with_constant_settings(settings: "LdapSettings") -> "LdapAuthProvider":
        return LdapAuthProvider(ConstantLdapSettingsLoader(settings))

    @staticmethod
    def with_settings_from_mongo(collection: Collection) -> "LdapAuthProvider":
        return LdapAuthProvider(MongoLdapSettingsLoader(collection, key=LdapAuthProvider.name))

    @property
    def settings(self) -> "LdapSettings":
        return self._settings_loader.get()

    def update_settings(self, new_settings: dict) -> None:
        self._settings_loader.set(new_settings)

    def is_enabled(self) -> bool:
        return self.settings.enabled

    def register(self, username: str, password: str, **settings) -> None:
        raise Exception("Registering users with LDAP is not supported")

    def login(self, username: str, password: str) -> Tuple[User, List[str]]:
        """
        Verifies the specified user credentials.
        Checks that the user is a member of at least one of the configured groups.
        """
        settings = self.settings
        user_dn, user_groups = self._find_user(username)

        if settings.admin_group_dn in user_groups:
            is_admin = True
        elif settings.user_group_dn in user_groups:
            is_admin = False
        else:
            raise ForbiddenException("Provided user is not a member of any authorized group")

        with settings.handle_ldap_exceptions(invalid_credentials_message=f"Failed to authenticate {user_dn=}"):
            settings.connect(bind=False).bind_s(user_dn, password)

        return User(
            username=username,
            auth_provider_name=self.name,
            is_admin=is_admin,
        ), list(user_groups)

    def _find_user(self, username: str) -> Tuple[str, Set[str]]:
        """
        :return: The user DN and the group DNs the user is a member of.
        """
        settings = self.settings
        ldap_connection = settings.connect(bind=True)
        user_filter = settings.filter.format(username=username)

        with settings.handle_ldap_exceptions(extra="finding user"):
            r = ldap_connection.search_s(
                settings.users_base,
                ldap.SCOPE_SUBTREE,
                user_filter,
                attrlist=[LDAP_MEMBER_IN_GROUP_ATTRIBUTE],
            )

        if len(r) == 0:
            raise UnauthorizedException(f"Failed to find user {username}")

        if len(r) > 1:
            raise UnauthorizedException(f"Username {username} does not appear to be unique. Check the config.")

        user_dn, user_object = r[0]

        if settings.use_ad_style_group_membership:
            groups = []
            with settings.handle_ldap_exceptions(extra="finding user groups"):
                for group_dn in [settings.admin_group_dn, settings.user_group_dn]:
                    if ldap_connection.search_s(
                        settings.users_base,
                        ldap.SCOPE_SUBTREE,
                        # Recursive search is extremely slow, optimizing by filtering only for the wanted groups
                        f"(&(memberOf:{LDAP_MATCHING_RULE_IN_CHAIN}:={group_dn})({user_filter}))",
                        attrlist=[""],
                    ):
                        groups.append(group_dn)
        elif LDAP_MEMBER_IN_GROUP_ATTRIBUTE in user_object:
            groups = [group_dn.decode() for group_dn in user_object[LDAP_MEMBER_IN_GROUP_ATTRIBUTE]]
        else:
            raise UnauthorizedException("User doesn't have a memberOf field; Their groups can't be determined")

        return user_dn, set(groups)

    def query_user_groups(self, username: str) -> List[str]:
        """
        Just returns the full list of groups the user is a member of. No authentication is done.
        """
        settings = self.settings

        user_dn, user_groups = self._find_user(username)

        if settings.use_ad_style_group_membership:
            with settings.handle_ldap_exceptions(extra="finding user groups"):
                r = settings.connect(bind=True).search_s(
                    settings.groups_base,
                    ldap.SCOPE_SUBTREE,
                    f"member:{LDAP_MATCHING_RULE_IN_CHAIN}:={user_dn}",
                    attrlist=[""],
                )
                user_groups = [group_dn for group_dn, _ in r]

        return list(user_groups)


# Like vanilla Python dataclasses, but with type enforcement.
@pydantic.dataclasses.dataclass(frozen=True)
class LdapSettings:
    """
    LDAP Authentication configuration.

    uri: The URI of the LDAP server; i.e. ldap://server.com:1337

    users_base: the common part of user DNs. For example, ou=users,dc=my-org,dc=co,dc=il
    groups_base: the common part of group DNs. For example, ou=groups,dc=my-org,dc=co,dc=il

    filter: an LDAP search query format string that will be used to find the DN of a user which attempts to log in.
           For example, (sAMAccountName={username}).
           The string must contain the `{username}` placeholder.

    bind_dn: the DN used to bind to the LDAP server for searching purposes.
    bind_password: password for the bind DN account.

    admin_group_dn: Members of this group will be considered admins of this system.
    user_group_dn: Members of this group will be considered regular non-admin users of this system.

    timeout_seconds: Limits the wait time for the LDAP server (initial connection / operations, like search).

    use_ad_style_group_membership:
        See https://ldapwiki.com/wiki/Active%20Directory%20User%20Related%20Searches#section-Active+Directory+User+Related+Searches-AllGroupsAUserIsAMemberOfIncludingNestedGroups
        This is an AD-specific extension that allows for recursive group membership check.
        For example, Group A contains Group B which contains User 1.
        This mode is unsupported in OopenLDAP.

    raw: Raw settings, as-is from the DB. Used in the UI to enable changing invalid settings.
    """

    enabled: bool
    uri: str
    users_base: str
    groups_base: str
    filter: str
    bind_dn: str
    bind_password: str
    admin_group_dn: str
    user_group_dn: str
    use_ad_style_group_membership: bool

    raw: Dict[str, Any]

    timeout_seconds: int = 10

    def connect(self, *, bind: bool = False) -> LDAPObject:
        if not self.enabled:
            raise ValueError("Cannot attempt to connect to the LDAP server when disabled")

        with self.handle_ldap_exceptions(invalid_credentials_message=f"Failed to bind using {self.bind_dn=}"):
            connection = ldap.initialize(self.uri)
            connection.set_option(ldap.OPT_TIMEOUT, self.timeout_seconds)
            connection.set_option(ldap.OPT_NETWORK_TIMEOUT, self.timeout_seconds)

            if bind:
                connection.bind_s(self.bind_dn, self.bind_password)

            return connection

    @classmethod
    def create(cls, raw: Dict[str, Any]) -> "LdapSettings":
        try:
            return LdapSettings(raw=raw, **raw)
        except (ValidationError, TypeError) as e:
            logger.exception("Given raw LDAP settings are invalid")
            raise InvalidSettingsException() from e

    @classmethod
    def create_or_disable(cls, raw: Dict[str, Any]) -> "LdapSettings":
        """
        Creates an instance of LdapSettings.
        In case the given raw settings are invalid, disabled settings will be created.
        """
        try:
            return cls.create(raw)
        except InvalidSettingsException:
            logger.warning("Creating disabled LDAP settings")
            return cls.create_disabled(raw)

    @classmethod
    def create_disabled(cls, raw: Dict[str, Any] = None) -> "LdapSettings":
        raw = raw or {}
        raw["enabled"] = False
        return LdapSettings(
            raw=raw or {},
            enabled=False,
            uri="",
            users_base="",
            groups_base="",
            filter="",
            bind_dn="",
            bind_password="",
            admin_group_dn="",
            user_group_dn="",
            use_ad_style_group_membership=False,
        )

    @contextlib.contextmanager
    def handle_ldap_exceptions(self, *, invalid_credentials_message: str = "Invalid Credentials", extra: str = ""):
        if extra:
            extra = f" ({extra})"

        try:
            yield
        except (ldap.TIMEOUT, ldap.TIMELIMIT_EXCEEDED) as e:
            raise UnauthorizedException(f"LDAP server at {self.uri} timed out" + extra) from e
        except ldap.SERVER_DOWN as e:
            raise UnauthorizedException(f"Failed to contact the LDAP server at {self.uri}" + extra) from e
        except ldap.INVALID_CREDENTIALS as e:
            raise UnauthorizedException(invalid_credentials_message + extra) from e
        except ldap.LDAPError as e:
            raise UnauthorizedException(f"Error while contacting the LDAP server at {self.uri}" + extra) from e
