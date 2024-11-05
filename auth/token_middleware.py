from typing import Optional, Tuple
import requests
from requests.adapters import BaseAdapter
from requests.auth import HTTPBasicAuth

from commonkit.logging.logging_config import LogConfig
log_config = LogConfig(__name__)
logger = log_config.logger

class TokenMiddleware(BaseAdapter):
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None

    def __init__(self, token_url: str, refresh_url: str, username: str, password: str, ba_username: str, ba_password: str, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_url = token_url
        self.refresh_url = refresh_url
        self.username = username
        self.password = password
        self.ba_username = ba_username
        self.ba_password = ba_password
        self.session = requests.Session()

    def send(self, request: requests.PreparedRequest, **kwargs):
        request.headers.update({'Id': "alo"})
        request.headers.update({'Authorization': f'Bearer {self.access_token}'})
        response = self.session.send(request, **kwargs)
        if response.status_code == 401:
            logger.info(f'Access token hết hạn, lấy access token {response.text}')
            success, self.refresh_token, self.access_token = TokenMiddleware.get_token(refresh_token=self.refresh_token, refresh_url=self.refresh_url, token_url=self.token_url, username=self.username, password=self.password, ba_username=self.ba_username, ba_password=self.ba_password)
            if success:
                request.headers.update({'Authorization': f'Bearer {self.access_token}'})
                response = self.session.send(request, **kwargs)
        return response

    @staticmethod
    def get_token(refresh_token: Optional[str], refresh_url: str, token_url: str, username: str, password: str, ba_username: str, ba_password: str) -> Tuple[bool, Optional[str], Optional[str]]:
        if refresh_token:
            data = {
                'refresh_token': refresh_token
            }
            response = requests.post(refresh_url, params=data, auth=HTTPBasicAuth(username=ba_username, password=ba_password))
            if response.status_code == 200 and response.json()["data"]:
                refresh_token = response.json()["data"]["refreshToken"]
                access_token = response.json()["data"]["accessToken"]
                return True, refresh_token, access_token
            else:
                logger.info(f"Refresh token hết hạn {response.text}")

        data = {
            'username': username,
            'password': password
        }
        response = requests.post(token_url, data=data, auth=HTTPBasicAuth(username=ba_username, password=ba_password))
        if response.status_code == 200 and response.json()["data"]:
            refresh_token = response.json()["data"]["refreshToken"]
            access_token = response.json()["data"]["accessToken"]
            return True, refresh_token, access_token
        else:
            logger.error(f'Lấy refresh token thất bại {response.text}')
            return False, None, None
