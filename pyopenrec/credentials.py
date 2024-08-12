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
        return all([self.access_token, self.uuid, self.token, self.random])

    @property
    def params(self) -> dict[str, Optional[str]]:
        """
        Return credentials as dict.
        """
        return {
            "access_token": self.access_token,
            "uuid": self.uuid,
            "token": self.token,
            "random": self.random,
        }

    def __repr__(self) -> str:
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
