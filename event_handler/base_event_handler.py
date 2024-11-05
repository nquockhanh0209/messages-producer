from typing import List

from commonkit.kafka.producer.base_producer import BaseProducer
from commonkit.websocket.base_event_handler import BaseEventHandler
from config.config import Config
from ws.websocket_client import WebsocketClient

from commonkit.logging.logging_config import LogConfig
log_config = LogConfig(__name__)
logger = log_config.logger


class BaseEventHandler(BaseEventHandler):
    config: Config
    producer: BaseProducer
    def __init__(self, event_types: List[str], ws_client: WebsocketClient, config: Config):
        super().__init__(event_types=event_types, ws_client=ws_client)
        self.config = Config()
        kafka_host = self.config.KAFKA_HOST+":"+self.config.KAFKA_PORT

        self.producer = BaseProducer(topic_name = event_types, bootstrap_servers=[kafka_host])
