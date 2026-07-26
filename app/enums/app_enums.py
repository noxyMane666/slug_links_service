from enum import Enum

class RequestStatus(str, Enum):
    Ok = "Ok"
    Error = "Error"