import threading
from commonkit.utilities.json_serializer import JSONSerializer
from config.config import Config
from event_handler.base_event_handler import BaseEventHandler
from ws.websocket_client import WebsocketClient


class EventHandler(BaseEventHandler):
    lock = threading.Lock()

    def __init__(self, event_type: str , ws_client: WebsocketClient, config: Config):
        super().__init__(event_type=event_type, ws_client=ws_client, config = config)

    def handle(self, message: dict):
        with self.lock:
            result_str = JSONSerializer.serialize_json_dic(dic=message)
            self.ws_client.send(data=result_str)
            data = JSONSerializer.string_to_dict(message['data'])
            self.producer.send(value_dict=data)
            