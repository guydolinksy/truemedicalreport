from typing import Optional, Set, Tuple

import ldap
import logbook
from ldap.ldapobject import LDAPObject
from pydantic import BaseModel, root_validator, Extra

from .exceptions import UnauthorizedException
from .user import User


logger = logbook.Logger(__name__)


class _LdapAuthSettings(BaseModel, extra=Extra.forbid):
    """
    LDAP Authentication configuration.

    uri: The URI of the LDAP server; i.e. ldap://server.com:1337
    base: the common part of each DNs. For example, dc=my-org,dc=co,dc=il
    filter: an LDAP search query format string that will be used to find the DN of a user which attempts to log in.
           For example, (sAMAccountName={username}).
           The string must contain the `{username}` placeholder.

    bind_dn: the DN used to bind to the LDAP server for searching purposes.
    bind_password: password for the bind DN account.

    admin_group_dn: Members of this group will be considered admins of this system.
    user_group_dn: Members of this group will be considered regular non-admin users of this system.
    """

    uri: str
    base: str
    filter: str

    bind_dn: str
    bind_password: str

    admin_group_dn: str
    user_group_dn: str


class LdapAuth(BaseModel, extra=Extra.forbid):
    enabled: bool
    settings: Optional[_LdapAuthSettings]

    @classmethod
    @root_validator
    def check_settings_are_present_if_enabled(cls, values: dict) -> dict:
        if values.get("enabled", False):
            assert "settings" in values

        return values

    def auth_with_groups(self, login_source: str, username: str, password: str) -> Optional[User]:
        """
        Verifies the specified user credentials.
        Checks that the user is a member of at least one of the configured groups.
        """
        connection = self._connect()

        user_dn, user_groups = self._find_user(connection, username)

        if self.settings.admin_group_dn in user_groups:
            is_admin = True
        elif self.settings.user_group_dn in user_groups:
            is_admin = False
        else:
            raise UnauthorizedException("Provided user is not a member of any authorized group")

        try:
            connection.bind_s(user_dn, password)
        except ldap.INVALID_CREDENTIALS:
            raise UnauthorizedException(f"Failed to authenticate {user_dn=}")

        return User(username=username, source=login_source, is_admin=is_admin, groups=list(user_groups))

    def _find_user(self, connection: LDAPObject, username: str) -> Tuple[str, Set[str]]:
        """
        :return: The user DN and the group DNs the user is a member of.
        """

        r = connection.search_s(self.settings.base, ldap.SCOPE_SUBTREE, self.settings.filter.format(username=username))

        if len(r) == 0:
            raise UnauthorizedException(f"Failed to find user {username}")

        if len(r) > 1:
            raise UnauthorizedException(f"Username {username} does not appear to be unique. Check the config.")

        user_dn, user_object = r[0]

        if "memberOf" not in user_object:
            raise UnauthorizedException("User doesn't have a memberOf field; Their groups can't be determined")

        groups = set(group_dn.decode() for group_dn in user_object['memberOf'])

        return user_dn, groups

    def _connect(self) -> LDAPObject:
        connection = ldap.initialize(self.settings.uri)

        if not connection.bind_s(self.settings.bind_dn, self.settings.bind_password):
            raise UnauthorizedException(f"Failed to bind using {self.settings.bind_dn=}")

        return connection
