import json


class OpenrecCredentials:
    """
    Credentials for openrec.tv.
    """
    access_token: str = None
    uuid: str = None
    token: str = None
    random: str = None

    @property
    def is_login(self) -> bool:
        return (
            self.access_token is not None
            and self.uuid is not None
            and self.token is not None
            and self.random is not None
        )

    @property
    def params(self) -> dict:
        """
        Return credentials as dict.
        """
        return {
            "access_token": self.access_token,
            "uuid": self.uuid,
            "token": self.token,
            "random": self.random,
        }

    def __str__(self) -> str:
        """
        Return credentials as json string.
        """
        return json.dumps(self.params)
