# tags.py
"""
This script defines all tags that can be retrieved to visualiser.
We have all tags here to for better organisation.

To add new tage follow these steps:
If it is completely new element add new tag to NetworkElementTags
Then create new class where you need to define attributes of element
"""
from enum import Enum


class NetworkElementTags(Enum):
    ANIM_TAG = 'anim'
    NODE_TAG = 'node'
    NU_TAG = 'nu'
    NONP2PLINKPROPERTIES_TAG = 'nonp2plinkproperties'
    IP_TAG = 'ip'
    ADDRESS_TAG = 'address'
    NCS_TAG = 'ncs'
    P_TAG = 'p'
    WPR_TAG = 'wpr'
    PR_TAG = 'pr'
    RES_TAG = 'res'
    LINK_TAG = 'link'
    IPV6_TAG = 'ipv6'


class AnimTags:
    VER_TAG = 'ver'
    FILE_TYPE_TAG = 'filetype'


class NodeTags:
    ID_TAG = 'id'
    SYS_ID_TAG = 'sysId'
    LOC_X_TAG = 'locX'
    LOC_Y_TAG = 'locY'
    LOC_Z_TAG = 'locZ'


class NuTags:
    P_TAG = 'p'
    T_TAG = 't'
    ID_TAG = 'id'
    COLOR_R_TAG = 'r'
    COLOR_G_TAG = 'g'
    COLOR_B_TAG = 'b'
    WIDTH_TAG = 'w'
    HEIGHT_TAG = 'h'
    COORD_X_TAG = 'x'
    COORD_Y_TAG = 'y'
    COORD_Z_TAG = 'z'
    DESCRIPTION_TAG = 'descr'


class NonP2pLinkPropertiesTags:
    ID_TAG = 'id'
    IP_ADDRESS_TAG = 'ipAddress'
    CHANNEL_TYPE_TAG = 'channelType'


class IpTags:
    N_TAG = 'n'


class AddressTags:
    IP_ADDRESS_TAG = 'address'


class NcsTags:
    NC_ID_TAG = 'ncId'
    N_TAG = 'n'
    T_TAG = 't'


class PTags:
    FROM_ID_TAG = 'fId'
    FB_TX_TAG = 'fbTx'
    LB_TX_TAG = 'lbTx'
    META_INFO_TAG = 'meta-info'
    TO_ID_TAG = 'tId'
    FB_RX_TAG = 'fbRx'
    LB_RX_TAG = 'lbRx'


class WprTags:
    U_ID_TAG = 'uId'
    T_ID_TAG = 'tId'
    FB_RX_TAG = 'fbRx'
    LB_RX_TAG = 'lbRx'


class PrTags:
    U_ID_TAG = 'uId'
    F_ID_TAG = 'fId'
    FB_TX_TAG = 'fbTx'
    META_INFO_TAG = 'meta-info'


class ResTags:
    RID_TAG = 'rid'
    P_TAG = 'p'


class LinkTags:
    FROM_ID_TAG = 'fromId'
    TO_ID_TAG = 'toId'
    FD_TAG = 'fd'
    TD_TAG = 'td'
    LD_TAG = 'ld'


class IpV6Tags:
    N_TAG = 'n'
