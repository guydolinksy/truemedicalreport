from backend.logics.user import User


class AuthProvider:
    name = NotImplemented

    def register(self, username: str, password: str) -> None:
        """
        Registers a new user. Not always supported - for example, LDAP is read-only;
        """
        raise NotImplementedError

    def login(self, username: str, password: str) -> User:
        """
        Logins a user.

        If the credentials are wrong or the user does not exist, UnauthorizedException should be thrown with appropriate
        reason set.
        """
        raise NotImplementedError

    def is_enabled(self) -> bool:
        return True
