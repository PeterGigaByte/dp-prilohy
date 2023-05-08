from enum import Enum


class StepType(Enum):
    WIRED_PACKET = "WIRED_PACKET",
    NODE_UPDATE = "NODE_UPDATE",
    WIRELESS_PACKET_RECEPTION = "WIRELESS_PACKET_RECEPTION",
    BROADCAST = "BROADCAST"


class NodeUpdateType(Enum):
    P = "POSITION",
    D = "DESCRIPTION",
    S = "SIZE",
    I = "INFORMATION"
    C = "COLOR"
