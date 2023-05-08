import json

from PyQt5.QtCore import QThread, pyqtSignal


from network_elements.elements import Anim, Address, Node, NodeUpdate, NonP2pLinkProperties, Ip, IpV6, WiredPacket, Ncs, \
    Link, Resource, WirelessPacketReception, Broadcaster
from network_elements.tags import NetworkElementTags, AnimTags, NodeTags, NuTags, NonP2pLinkPropertiesTags, PTags, \
    WprTags, NcsTags, LinkTags, ResTags, PrTags, IpTags, IpV6Tags

prefix = '@'


def json_parse_nodes(data):
    data_list = []
    for node in data.get(NetworkElementTags.NODE_TAG.value) or []:
        data_list.append(Node(node.get(prefix + NodeTags.ID_TAG),
                              node.get(prefix + NodeTags.SYS_ID_TAG),
                              node.get(prefix + NodeTags.LOC_X_TAG),
                              node.get(prefix + NodeTags.LOC_Y_TAG),
                              node.get(prefix + NodeTags.LOC_Z_TAG)
                              ))
    return data_list


def json_parse_nu(data):
    data_list = []
    for nu in data.get(NetworkElementTags.NU_TAG.value) or []:
        data_list.append(NodeUpdate(
            nu.get(prefix + NuTags.P_TAG),
            nu.get(prefix + NuTags.T_TAG),
            nu.get(prefix + NuTags.ID_TAG),
            nu.get(prefix + NuTags.COLOR_R_TAG),
            nu.get(prefix + NuTags.COLOR_G_TAG),
            nu.get(prefix + NuTags.COLOR_B_TAG),
            nu.get(prefix + NuTags.WIDTH_TAG),
            nu.get(prefix + NuTags.HEIGHT_TAG),
            nu.get(prefix + NuTags.COORD_X_TAG),
            nu.get(prefix + NuTags.COORD_Y_TAG),
            nu.get(prefix + NuTags.COORD_Z_TAG),
            nu.get(prefix + NuTags.DESCRIPTION_TAG)
        ))
    return data_list


def json_parse_non_link_properties(data):
    data_list = []
    for non_link_property in data.get(NetworkElementTags.NONP2PLINKPROPERTIES_TAG.value) or []:
        data_list.append(NonP2pLinkProperties(non_link_property.get(prefix + NonP2pLinkPropertiesTags.ID_TAG),
                                              non_link_property.get(prefix + NonP2pLinkPropertiesTags.IP_ADDRESS_TAG),
                                              non_link_property.get(prefix + NonP2pLinkPropertiesTags.CHANNEL_TYPE_TAG)
                                              ))
    return data_list


def json_parse_ip(data):
    data_list = []
    for ip in data.get(NetworkElementTags.IP_TAG.value) or []:
        data_list.append(Ip(ip.get(prefix + IpTags.N_TAG),
                            json_parse_address(ip.get(NetworkElementTags.ADDRESS_TAG.value))
                            ))
    return data_list


def json_parse_ipv(data):
    data_list = []
    for ipv in data.get(NetworkElementTags.IPV6_TAG.value) or []:
        data_list.append(IpV6(ipv.get(prefix + IpV6Tags.N_TAG),
                              json_parse_address(ipv.get(NetworkElementTags.ADDRESS_TAG.value))
                              ))
    return data_list


def json_parse_p(data):
    data_list = []
    for p in data.get(NetworkElementTags.P_TAG.value) or []:
        data_list.append(WiredPacket(p.get(prefix + PTags.FROM_ID_TAG),
                                     p.get(prefix + PTags.FB_TX_TAG),
                                     p.get(prefix + PTags.LB_TX_TAG),
                                     p.get(prefix + PTags.META_INFO_TAG),
                                     p.get(prefix + PTags.TO_ID_TAG),
                                     p.get(prefix + PTags.FB_RX_TAG),
                                     p.get(prefix + PTags.LB_RX_TAG)
                                     ))
    return data_list


def json_parse_wpr(data):
    data_list = []
    for wpr in data.get(NetworkElementTags.WPR_TAG.value) or []:
        data_list.append(WirelessPacketReception(wpr.get(prefix + WprTags.U_ID_TAG),
                                                 wpr.get(prefix + WprTags.T_ID_TAG),
                                                 wpr.get(prefix + WprTags.FB_RX_TAG),
                                                 wpr.get(prefix + WprTags.LB_RX_TAG)
                                                 ))
    return data_list


def json_parse_pr(data):
    data_list = []
    for pr in data.get(NetworkElementTags.PR_TAG.value) or []:
        data_list.append(Broadcaster(
            pr.get(prefix + PrTags.U_ID_TAG),
            pr.get(prefix + PrTags.F_ID_TAG),
            pr.get(prefix + PrTags.FB_TX_TAG),
            pr.get(prefix + PrTags.META_INFO_TAG)
        ))
    return data_list


def json_parse_res(data):
    data_list = []
    for res in data.get(NetworkElementTags.RES_TAG.value) or []:
        data_list.append(Resource(
            res.get(prefix + ResTags.RID_TAG),
            res.get(prefix + ResTags.P_TAG),
        ))
    return data_list


def json_parse_link(data):
    data_list = []
    data = data.get(NetworkElementTags.LINK_TAG.value)
    if data is not None:
        data_list.append(Link(data.get(prefix + LinkTags.FROM_ID_TAG),
                              data.get(prefix + LinkTags.TO_ID_TAG),
                              data.get(prefix + LinkTags.FD_TAG),
                              data.get(prefix + LinkTags.TD_TAG),
                              data.get(prefix + LinkTags.LD_TAG)
                              ))
    return data_list


def json_parse_nsc(data):
    data_list = [Ncs(data.get(NetworkElementTags.NCS_TAG.value).get(prefix + NcsTags.NC_ID_TAG),
                     data.get(NetworkElementTags.NCS_TAG.value).get(prefix + NcsTags.N_TAG),
                     data.get(NetworkElementTags.NCS_TAG.value).get(prefix + NcsTags.T_TAG)
                     )]
    return data_list


def json_parse_address(data):
    data_list = []
    for address in data or []:
        data_list.append(Address(address))
    return data_list


class JsonParser(QThread):
    parsed_data_signal = pyqtSignal(object)

    def __init__(self, bottom_dock_widget):
        super().__init__()
        self.path = None
        self.bottom_dock_widget = bottom_dock_widget
        self.anim = None
        self.none_type = None

    def run(self):
        self.bottom_dock_widget.log('Json parser begin.')
        self.bottom_dock_widget.log('File path: {0}'.format(self.path))
        # Opening JSON file
        f = open(self.path)

        # returns JSON object as
        # a dictionary
        data = json.load(f)

        data = data[NetworkElementTags.ANIM_TAG.value]
        # Iterating through the json
        # list
        # for i in data['emp_details']:
        #     print(i)
        anim = Anim(data.get(prefix + AnimTags.VER_TAG),
                    data.get(prefix + AnimTags.FILE_TYPE_TAG)
                    )
        content = []
        content.extend(json_parse_nodes(data))
        content.extend(json_parse_nu(data))
        content.extend(json_parse_non_link_properties(data))
        content.extend(json_parse_ip(data))
        content.extend(json_parse_ipv(data))
        content.extend(json_parse_p(data))
        content.extend(json_parse_wpr(data))
        content.extend(json_parse_pr(data))
        content.extend(json_parse_res(data))
        content.extend(json_parse_link(data))
        content.extend(json_parse_nsc(data))
        anim.content = content
        # Closing file
        f.close()
        self.bottom_dock_widget.log('Json parser end.')
        self.parsed_data_signal.emit(anim)

    def parse(self, path, batch_size):
        self.path = path
        self.start()
