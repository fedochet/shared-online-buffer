from channels.routing import route
from buffer.consumers import ws_connect, ws_disconnect, ws_message

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_message),
    route('websocket.disconnect', ws_disconnect)
]