import os
from threading import Lock

import logging

from commonkit.utilities.net_utilities import NetUtilities
logger = logging.getLogger(__name__)


class ConfigMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ConfigMeta):
    STREAMING_SERVICE_ADDRESS: str
    STREAMING_SERVICE_RTMP_PORT: int
    STREAMING_SERVICE_RTSP_PORT: int

    def __init__(self):
        self.LOCAL_DATABASE_URL = "sqlite:///database.db"
        if "REST_HOST" in os.environ:
            self.REST_HOST = os.environ["REST_HOST"]
            self.VMS_WS_HOST = f"{os.environ['REST_HOST'].replace('https://', 'wss://').replace('http://', 'ws://')}"
        if "AUTH_SERVICE_TOKEN_ENDPOINT" in os.environ:
            self.AUTH_TOKEN_URL = f"{self.REST_HOST}{os.environ['AUTH_SERVICE_TOKEN_ENDPOINT']}"
        if "AUTH_SERVICE_REFRESH_TOKEN_ENDPOINT" in os.environ:
            self.AUTH_REFRESH_URL = f"{self.REST_HOST}{os.environ['AUTH_SERVICE_REFRESH_TOKEN_ENDPOINT']}"
        if "AUTH_USERNAME" in os.environ:
            self.AUTH_USERNAME = os.environ["AUTH_USERNAME"]
        if "AUTH_PASSWORD" in os.environ:
            self.AUTH_PASSWORD = os.environ["AUTH_PASSWORD"]
        if "AUTH_BA_USERNAME" in os.environ:
            self.AUTH_BA_USERNAME = os.environ["AUTH_BA_USERNAME"]
        if "AUTH_BA_PASSWORD" in os.environ:
            self.AUTH_BA_PASSWORD = os.environ["AUTH_BA_PASSWORD"]
        if "VMS_USER_ID" in os.environ:
            self.VMS_USER_ID = os.environ["VMS_USER_ID"]
        if "VMS_ENDPOINT" in os.environ:
            self.VMS_REST_HOST = f"{self.REST_HOST}{os.environ['VMS_ENDPOINT']}"
        if "MINIO_HOST" in os.environ:
            self.MINIO_HOST = os.environ["MINIO_HOST"].replace(
                "https://", "").replace("http://", "")
            self.MINIO_SSL_ENABLE = "https" in os.environ["MINIO_HOST"]
        if "MINIO_ACCESS_KEY" in os.environ:
            self.MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
        if "MINIO_SECRET_KEY" in os.environ:
            self.MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
        if "MINIO_PART_SIZE" in os.environ:
            self.MINIO_PART_SIZE = os.environ["MINIO_PART_SIZE"]
        if "MINIO_VIDEOS_BUCKET_NAME" in os.environ:
            self.MINIO_VIDEOS_BUCKET_NAME = os.environ["MINIO_VIDEOS_BUCKET_NAME"]
        else:
            self.MINIO_VIDEOS_BUCKET_NAME = "videos"

        if "MINIO_IMAGES_BUCKET_NAME" in os.environ:
            self.MINIO_IMAGES_BUCKET_NAME = os.environ["MINIO_IMAGES_BUCKET_NAME"]
        else:
            self.MINIO_IMAGES_BUCKET_NAME = "images"

        if "SERVICE_NAME" in os.environ:
            self.SERVICE_NAME = os.environ["SERVICE_NAME"]

        if "SERVICE_IP_ADDRESS" in os.environ:
            self.SERVICE_IP_ADDRESS = os.environ["SERVICE_IP_ADDRESS"]
        else:
            self.SERVICE_IP_ADDRESS = NetUtilities.get_ip_address()

        if "SERVICE_MAC_ADDRESS" in os.environ:
            self.SERVICE_MAC_ADDRESS = os.environ["SERVICE_MAC_ADDRESS"]
        else:
            self.SERVICE_MAC_ADDRESS = NetUtilities.get_mac_address()

        if "SERVICE_HOST_NAME" in os.environ:
            self.SERVICE_HOST_NAME = os.environ["SERVICE_HOST_NAME"]
        else:
            self.SERVICE_HOST_NAME = NetUtilities.get_host_name()
        
        if "KAFKA_PORT" in os.environ:
            self.KAFKA_PORT = os.environ["KAFKA_PORT"]

        if "KAFKA_HOST" in os.environ:
            self.KAFKA_HOST = os.environ["KAFKA_HOST"]

        logger.info(self.__dict__)
