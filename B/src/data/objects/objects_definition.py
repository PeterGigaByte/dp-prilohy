from enum import Enum


class Tags(Enum):
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


class Anim:
    has_ending = True
    VER_TAG = 'ver'
    FILE_TYPE_TAG = 'filetype'

    def __init__(self, name, version, filetype, content=''):
        self.name = name
        self.version = version
        self.filetype = filetype
        # List of objects
        self.content = content

    def __str__(self):
        return '(name: {0}, version: {1}, filetype: {2}, content: {3})'.format(self.name, self.version, self.filetype,
                                                                               self.content)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, i):
        return self


class Node:
    has_ending = False
    ID_TAG = 'id'
    SYS_ID_TAG = 'sysId'
    LOC_X_TAG = 'locX'
    LOC_Y_TAG = 'locY'

    def __init__(self, name, id_node, sys_id, loc_x, loc_y):
        self.name = name
        self.id = id_node
        self.sys_id = sys_id
        self.loc_x = loc_x
        self.loc_y = loc_y

    def __str__(self):
        return '(name: {0}, id: {1}, sysId: {2}, locX: {3}, locY: {4})'.format(self.name, self.id, self.sys_id,
                                                                               self.loc_x, self.loc_y)

    def __repr__(self):
        return '(name: {0}, id: {1}, sysId: {2}, locX: {3}, locY: {4})'.format(self.name, self.id, self.sys_id,
                                                                               self.loc_x, self.loc_y)

    def __getitem__(self, i):
        return self


class Nu:
    has_ending = False
    # Parameters
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
    DESCRIPTION_TAG = 'descr'

    def __init__(self, name, p, t, id_nu, r=None, g=None, b=None, w=None, h=None, x=None, y=None, descr=None):
        self.name = name
        self.p = p
        self.t = t
        self.id = id_nu
        self.r = r
        self.g = g
        self.b = b
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.descr = descr

    def __str__(self):
        return '(name: {0}, p: {1}, t: {2}, id: {3}, r: {4}, g: {5}, b: {6}, w: {7}, h: {8}, x: {9}, y: {10}, ' \
               'descr: {11})'. \
            format(self.name, self.p, self.t, self.id, self.r, self.g, self.b, self.w, self.h, self.x, self.y,
                   self.descr)

    def __repr__(self):
        return '(name: {0}, p: {1}, t: {2}, id: {3}, r: {4}, g: {5}, b: {6}, w: {7}, h: {8}, x: {9}, y: {10}, ' \
               'descr: {11})'. \
            format(self.name, self.p, self.t, self.id, self.r, self.g, self.b, self.w, self.h, self.x, self.y,
                   self.descr)

    def __getitem__(self, i):
        return self


# Nonp2plinkproperties
class NonP2pLinkProperties:
    has_ending = False
    # Parameters
    ID_TAG = 'id'
    IP_ADDRESS_TAG = 'ipAddress'
    CHANNEL_TYPE_TAG = 'channelType'

    def __init__(self, name, id_properties, ip_address, channel_type):
        self.name = name
        self.id = id_properties
        self.ip_address = ip_address
        self.channel_type = channel_type

    def __str__(self):
        return '(name: {0}, id: {1}, ipAddress: {2}, channelType: {3})'.format(self.name, self.id, self.ip_address,
                                                                               self.channel_type)

    def __repr__(self):
        return '(name: {0}, id: {1}, ipAddress: {2}, channelType: {3})'.format(self.name, self.id, self.ip_address,
                                                                               self.channel_type)

    def __getitem__(self, i):
        return self


class Ip:
    has_ending = True
    # Parameters
    N_TAG = 'n'

    def __init__(self, name, n, addresses=None):
        if addresses is None:
            addresses = []
        self.name = name
        self.n = n
        # List of Objects
        self.addresses = addresses

    def __str__(self):
        return '(name: {0}, n: {1}, addresses: {2})'.format(self.name, self.n, self.addresses)

    def __repr__(self):
        return '(name: {0}, n: {1}, addresses: {2})'.format(self.name, self.n, self.addresses)

    def __getitem__(self, i):
        return self


class Address:
    has_ending = True
    # Parameters
    IP_ADDRESS_TAG = 'address'

    def __init__(self, name, ip_address):
        self.name = name
        self.ip_address = ip_address

    def __str__(self):
        return '(name: {0}, address: {1})'.format(self.name, self.ip_address)

    def __repr__(self):
        return '(name: {0}, address: {1})'.format(self.name, self.ip_address)

    def __getitem__(self, i):
        return self


class Ncs:
    has_ending = False
    # Parameters
    NC_ID_TAG = 'ncId'
    N_TAG = 'n'
    T_TAG = 't'

    def __init__(self, name, nc_id, n, t):
        self.name = name
        self.nc_id = nc_id
        self.n = n
        self.t = t

    def __str__(self):
        return '(name: {0}, ncId: {1}, n: {2}, t: {3}'.format(self.name, self.nc_id, self.n, self.t)

    def __repr__(self):
        return '(name: {0}, ncId: {1}, n: {2}, t: {3}'.format(self.name, self.nc_id, self.n, self.t)

    def __getitem__(self, i):
        return self


class P:
    has_ending = False
    # Parameters
    FROM_ID_TAG = 'fId'
    FB_TX_TAG = 'fbTx'
    META_INFO_TAG = 'meta_info'
    TO_ID_TAG = 'tId'
    FB_RX_TAG = 'fbRx'
    LB_RX_TAG = 'lbRx'

    def __init__(self, name, f_id, fb_tx, meta_info, t_id, fb_rx, lb_rx):
        self.name = name
        self.f_id = f_id
        self.fb_tx = fb_tx
        # meta-info is real name
        self.meta_info = meta_info
        self.t_id = t_id
        self.fb_rx = fb_rx
        self.lb_rx = lb_rx

    def __str__(self):
        return '(name: {0}, fId: {1}, fbTx: {2}, meta_info: {3}, tId: {4}, fbRx: {5}, lbRx: {6})'.format(self.name,
                                                                                                         self.f_id,
                                                                                                         self.fb_tx,
                                                                                                         self.meta_info,
                                                                                                         self.t_id,
                                                                                                         self.fb_rx,
                                                                                                         self.lb_rx)

    def __repr__(self):
        return '(name: {0}, fId: {1}, fbTx: {2}, meta_info: {3}, tId: {4}, fbRx: {5}, lbRx: {6})'.format(self.name,
                                                                                                         self.f_id,
                                                                                                         self.fb_tx,
                                                                                                         self.meta_info,
                                                                                                         self.t_id,
                                                                                                         self.fb_rx,
                                                                                                         self.lb_rx)

    def __getitem__(self, i):
        return self


class Wpr:
    has_ending = False
    # Parameters
    U_ID_TAG = 'uId'
    T_ID_TAG = 'tId'
    FB_RX_TAG = 'fbRx'
    LB_RX_TAG = 'lbRx'

    def __init__(self, name, u_id, t_id, fb_rx, lb_rx):
        self.name = name
        self.u_id = u_id
        self.t_id = t_id
        self.fb_rx = fb_rx
        self.lb_rx = lb_rx

    def __str__(self):
        return '(name: {0}, uId: {1}, tId: {2}, fbRx: {3}, lbRx: {4})'.format(self.name,
                                                                              self.u_id,
                                                                              self.t_id,
                                                                              self.fb_rx,
                                                                              self.lb_rx,
                                                                              )

    def __repr__(self):
        return '(name: {0}, uId: {1}, tId: {2}, fbRx: {3}, lbRx: {4})'.format(self.name,
                                                                              self.u_id,
                                                                              self.t_id,
                                                                              self.fb_rx,
                                                                              self.lb_rx,
                                                                              )

    def __getitem__(self, i):
        return self


class Pr:
    has_ending = False
    # Parameters
    U_ID_TAG = 'uId'
    F_ID_TAG = 'fId'
    FB_TX_TAG = 'fbTx'
    META_INFO_TAG = 'meta_info'

    def __init__(self, name, u_id, f_id, fb_tx, meta_info):
        self.name = name
        self.u_id = u_id
        self.f_id = f_id
        self.fb_tx = fb_tx
        # meta-info
        self.meta_info = meta_info

    def __str__(self):
        return '(name: {0}, uId: {1}, fId: {2}, fbTx: {3}, meta_info: {4})'.format(self.name,
                                                                                   self.u_id,
                                                                                   self.f_id,
                                                                                   self.fb_tx,
                                                                                   self.meta_info
                                                                                   )

    def __repr__(self):
        return '(name: {0}, uId: {1}, fId: {2}, fbTx: {3}, meta_info: {4})'.format(self.name,
                                                                                   self.u_id,
                                                                                   self.f_id,
                                                                                   self.fb_tx,
                                                                                   self.meta_info
                                                                                   )

    def __getitem__(self, i):
        return self


class Res:
    has_ending = False
    # Parameters
    RID_TAG = 'rid'
    P_TAG = 'p'

    def __init__(self, name, rid, p):
        self.name = name
        self.rid = rid
        self.p = p

    def __str__(self):
        return '(name: {0}, rid: {1}, p: {2})'.format(self.name,
                                                      self.rid,
                                                      self.p
                                                      )

    def __repr__(self):
        return '(name: {0}, rid: {1}, p: {2})'.format(self.name,
                                                      self.rid,
                                                      self.p
                                                      )

    def __getitem__(self, i):
        return self


class Link:
    has_ending = False
    # Parameters
    FROM_ID_TAG = 'fromId'
    TO_ID_TAG = 'toId'
    FD_TAG = 'fd'
    TD_TAG = 'td'
    LD_TAG = 'ld'

    def __init__(self, name, from_id, to_id, fd, td, ld):
        self.name = name
        self.from_id = from_id
        self.to_id = to_id
        self.fd = fd
        self.td = td
        self.ld = ld

    def __str__(self):
        return '(name: {0}, fromId: {1}, toId: {2}, fd: {3}, td: {4}, ld: {5})'.format(self.name,
                                                                                       self.from_id,
                                                                                       self.to_id,
                                                                                       self.fd,
                                                                                       self.td,
                                                                                       self.ld
                                                                                       )

    def __repr__(self):
        return '(name: {0}, fromId: {1}, toId: {2}, fd: {3}, td: {4}, ld: {5})'.format(self.name,
                                                                                       self.from_id,
                                                                                       self.to_id,
                                                                                       self.fd,
                                                                                       self.td,
                                                                                       self.ld
                                                                                       )

    def __getitem__(self, i):
        return self


class IpV6:
    has_ending = True
    # Parameters
    N_TAG = 'n'

    def __init__(self, name, n, addresses=None):
        if addresses is None:
            addresses = []
        self.name = name
        self.n = n
        # List of Objects
        self.addresses = addresses

    def __str__(self):
        return '(name: {0}, n: {1}, addresses: {2})'.format(self.name,
                                                            self.n,
                                                            self.addresses
                                                            )

    def __repr__(self):
        return '(name: {0}, n: {1}, addresses: {2})'.format(self.name,
                                                            self.n,
                                                            self.addresses
                                                            )

    def __getitem__(self, i):
        return self
