from datetime import datetime
from enum import Enum

class Type(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2


def log(type,message):
    file = open("./log/events.log","a")
    file.write(f"{Type(type).name} --- [{datetime.now(tz=None)}]: {message} \n")
    file.close