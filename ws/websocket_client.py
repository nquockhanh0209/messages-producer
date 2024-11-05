from auth.token_middleware import TokenMiddleware
from typing import Callable, Optional
from commonkit.websocket.websocket_base_client import WebsocketBaseClient
from commonkit.logging.logging_config import LogConfig
log_config = LogConfig(__name__)
logger = log_config.logger


class WebsocketClient(WebsocketBaseClient):

    event_callback: Optional[Callable[[dict], None]]
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None

    def __init__(self, url: str, event_callback: Optional[Callable[[dict], None]] = None,
                 token_url: Optional[str] = None, refresh_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None, ba_username: Optional[str] = None, ba_password: Optional[str] = None,
                 user_id: Optional[str] = None):
        super().__init__(url=url, event_callback=event_callback)
        self.token_url = token_url
        self.refresh_url = refresh_url
        self.username = username
        self.password = password
        self.ba_username = ba_username
        self.ba_password = ba_password
        self.user_id = user_id

    def on_unauthorized(self):
        super().on_unauthorized()
        if self.token_url and self.refresh_url and self.username and self.password and self.ba_username and self.ba_password:
            logger.debug(f'Access token hết hạn, lấy access token')
            success, self.refresh_token, self.access_token = TokenMiddleware.get_token(refresh_token=self.refresh_token,
                                                                                       refresh_url=self.refresh_url,
                                                                                       token_url=self.token_url,
                                                                                       username=self.username,
                                                                                       password=self.password,
                                                                                       ba_username=self.ba_username,
                                                                                       ba_password=self.ba_password)
            self.header.update(
                {'Authorization': f'Bearer {self.access_token}'})

        if self.user_id:
            logger.debug(f'update user id')
            self.header.update({'Id': f'{self.user_id}'})
