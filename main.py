from commonkit.config import Config
from commonkit.system_monitor.system_monitor import SystemMonitor
from event_handler.event_handler import EventHandler
from event_handler.event_list import EventList
from ws.websocket_client import WebsocketClient


class App:
    config: Config
    mac: str
    def __init__(self):
        self.config = Config()
        self.mac = "123"
        ws_url = f"{self.config.VMS_WS_HOST}/service/{self.mac}"
        ws_client = WebsocketClient(
            url=ws_url, user_id=self.config.VMS_USER_ID)
        
        list_event = EventList.allow_event
        for event in list_event:
            event_handler = EventHandler(event_type=event, ws_client = ws_client, config= self.config)
            ws_client.subscribe(event_handler)
        ws_client.connect_background()

        system_monitor = SystemMonitor()
        system_monitor.start()


