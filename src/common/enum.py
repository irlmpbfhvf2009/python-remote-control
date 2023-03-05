from enum import Enum
from src.common import utils

class General(Enum):
    IP = utils.getIP()
    RECV_SIZE = 1024
    PORT = 7777
    WINDOW_NAME = 'window'
    RYAN_IP = '192.168.0.66'