import json
from typing import Optional


class OpenrecCredentials:
    """
    Credentials for openrec.tv.
    """

    access_token: Optional[str] = None
    uuid: Optional[str] = None
    token: Optional[str] = None
    random: Optional[str] = None

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

    def load(self, json_str: str) -> None:
        """
        Load credentials from json string.

        Args:
            json_str (str): saved credentials as json string
        """
        params = json.loads(json_str)
        self.access_token = params["access_token"]
        self.uuid = params["uuid"]
        self.token = params["token"]
        self.random = params["random"]
