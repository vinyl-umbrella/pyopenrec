from typing import Optional

from .user import User


class Comment:
    """
    Comment class.
    """
    id: int = None
    message: str = None
    posted_at: str = None  # e.g. "2021-08-01T12:00:00.000Z"
    user: User = None
    stamp: dict = None
    capture: dict = None

    def __init__(
        self,
        comment_from_rest: Optional[dict] = None,
        comment_from_ws: Optional[dict] = None,
    ):
        """
        Openrec comment object.
        Args:
            comment_from_rest (dict, optional): comment from rest api
            comment_from_ws (dict, optional): comment from websocket
        """

        # set comment info from rest api
        if comment_from_rest:
            self.id = comment_from_rest.get("id", None)
            self.message = comment_from_rest.get("message", None)
            self.posted_at = comment_from_rest.get(
                "posted_at", None
            ) or comment_from_rest.get("created_at", None)

            self.stamp = comment_from_rest.get("stamp", None)
            self.capture = comment_from_rest.get("capture", None)

            self.user = User(
                comment_from_rest["user"]["id"], comment_from_rest.get("user", None)
            )

        # set comment info from websocket
        elif comment_from_ws:
            self.id = comment_from_ws.get("chat_id", None)
            self.message = comment_from_ws.get("message", None)
            self.posted_at = comment_from_ws.get("message_dt", None)
            self.stamp = comment_from_ws.get("stamp", None)
            self.capture = comment_from_ws.get("capture", None)

            user_data = {
                "id": comment_from_ws.get("user_key", None),
                "nickname": comment_from_ws.get("user_name", None),
                "l_icon_image_url": comment_from_ws.get("user_icon", None),
                "is_premium": comment_from_ws.get("is_premium", None),
                "is_fresh": comment_from_ws.get("is_fresh", None),
                "is_warned": comment_from_ws.get("is_warned", None),
            }
            self.user = User(comment_from_ws.get("user_key", None), user_data)
