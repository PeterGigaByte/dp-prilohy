from xml.dom.minidom import parse

from PyQt5.QtCore import QThread, pyqtSignal

from network_elements.elements import (
    Address, Anim, Ip, IpV6, Link, Ncs, Node, NonP2pLinkProperties,
    NodeUpdate, WiredPacket, Broadcaster, Resource, WirelessPacketReception
)
from network_elements.tags import NetworkElementTags, AnimTags, NodeTags, NuTags, NonP2pLinkPropertiesTags, AddressTags, \
    IpTags, IpV6Tags, NcsTags, PTags, WprTags, PrTags, ResTags, LinkTags


class DomXmlParser(QThread):
    parsed_data_signal = pyqtSignal(object)

    @staticmethod
    def get_attribute_with_none(node, attribute_name):
        attr_value = node.getAttribute(attribute_name)
        return None if attr_value == "" else attr_value

    def __init__(self, bottom_dock_widget):
        super().__init__()
        self.xml_file_path = None
        self.bottom_dock_widget = bottom_dock_widget
        self.anim = None
        self.none_type = None

    def parse(self, xml_file_path, batch_size):
        self.xml_file_path = xml_file_path
        self.start()

    def run(self):
        self.bottom_dock_widget.log('Xml DOM parser begin.')
        self.bottom_dock_widget.log('File path: {0}'.format(self.xml_file_path))
        root = parse(self.xml_file_path)

        # anim tag
        anim = dom_parse_anim(root)
        anim_content = []
        anim_content.extend(dom_parse_node(root))
        anim_content.extend(dom_parse_nu(root))
        anim_content.extend(dom_parse_non_link_properties(root))
        anim_content.extend(dom_parse_ip(root))
        anim_content.extend(dom_parse_ipv(root))
        anim_content.extend(dom_parse_p(root))
        anim_content.extend(dom_parse_wpr(root))
        anim_content.extend(dom_parse_pr(root))
        anim_content.extend(dom_parse_res(root))
        anim_content.extend(dom_parse_link(root))
        anim_content.extend(dom_parse_nsc(root))
        anim.content = anim_content
        self.bottom_dock_widget.log(f'NoneType tags : {self.none_type}')
        self.bottom_dock_widget.log('Xml DOM parser end.')
        self.parsed_data_signal.emit(anim)


def dom_parse_anim(data):
    anim_node = data.childNodes[0]
    return Anim(DomXmlParser.get_attribute_with_none(anim_node, AnimTags.VER_TAG),
                DomXmlParser.get_attribute_with_none(anim_node, AnimTags.FILE_TYPE_TAG)
                )


def dom_parse_node(data):
    nodes = data.getElementsByTagName(NetworkElementTags.NODE_TAG.value)
    data_list = []
    for node in nodes:
        data_list.append(Node(DomXmlParser.get_attribute_with_none(node, NodeTags.ID_TAG),
                              DomXmlParser.get_attribute_with_none(node, NodeTags.SYS_ID_TAG),
                              DomXmlParser.get_attribute_with_none(node, NodeTags.LOC_X_TAG),
                              DomXmlParser.get_attribute_with_none(node, NodeTags.LOC_Y_TAG),
                              DomXmlParser.get_attribute_with_none(node, NodeTags.LOC_Z_TAG)
                              ))
    return data_list


def dom_parse_nu(data):
    nus = data.getElementsByTagName(NetworkElementTags.NU_TAG.value)
    data_list = []
    for nu in nus:
        data_list.append(NodeUpdate(DomXmlParser.get_attribute_with_none(nu, NuTags.P_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.T_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.ID_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.COLOR_R_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.COLOR_G_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.COLOR_B_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.WIDTH_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.HEIGHT_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.COORD_X_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.COORD_Y_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.COORD_Z_TAG),
                                    DomXmlParser.get_attribute_with_none(nu, NuTags.DESCRIPTION_TAG),
                                    ))
    return data_list


def dom_parse_non_link_properties(data):
    non_link_properties_list = data.getElementsByTagName(NetworkElementTags.NONP2PLINKPROPERTIES_TAG.value)
    data_list = []
    for non_link_property in non_link_properties_list:
        data_list.append(NonP2pLinkProperties(
            DomXmlParser.get_attribute_with_none(non_link_property, NonP2pLinkPropertiesTags.ID_TAG),
            DomXmlParser.get_attribute_with_none(non_link_property, NonP2pLinkPropertiesTags.IP_ADDRESS_TAG),
            DomXmlParser.get_attribute_with_none(non_link_property, NonP2pLinkPropertiesTags.CHANNEL_TYPE_TAG)
        ))
    return data_list


def dom_parse_ip(data):
    ip_list = data.getElementsByTagName(NetworkElementTags.IP_TAG.value)
    data_list = []
    for ip in ip_list:
        data_list.append(Ip(DomXmlParser.get_attribute_with_none(ip, IpTags.N_TAG),
                            dom_parse_address(ip)
                            ))
    return data_list


def dom_parse_ipv(data):
    ipv_list = data.getElementsByTagName(NetworkElementTags.IPV6_TAG.value)
    data_list = []
    for ipv in ipv_list:
        data_list.append(IpV6(DomXmlParser.get_attribute_with_none(ipv, IpV6Tags.N_TAG),
                              dom_parse_address(ipv)
                              ))
    return data_list


def dom_parse_address(data):
    address_list = data.getElementsByTagName(NetworkElementTags.ADDRESS_TAG.value)
    data_list = []
    for address in address_list:
        data_list.append(Address(address.childNodes[0].nodeValue,
                                 ))
    return data_list


def dom_parse_nsc(data):
    nsc_list = data.getElementsByTagName(NetworkElementTags.NCS_TAG.value)
    data_list = []
    for nsc in nsc_list:
        data_list.append(Ncs(DomXmlParser.get_attribute_with_none(nsc, NcsTags.NC_ID_TAG),
                             DomXmlParser.get_attribute_with_none(nsc, NcsTags.N_TAG),
                             DomXmlParser.get_attribute_with_none(nsc, NcsTags.T_TAG)
                             ))
    return data_list


def dom_parse_p(data):
    p_list = data.getElementsByTagName(NetworkElementTags.P_TAG.value)
    data_list = []
    for p in p_list:
        data_list.append(WiredPacket(DomXmlParser.get_attribute_with_none(p, PTags.FROM_ID_TAG),
                                     DomXmlParser.get_attribute_with_none(p, PTags.FB_TX_TAG),
                                     DomXmlParser.get_attribute_with_none(p, PTags.LB_TX_TAG),
                                     DomXmlParser.get_attribute_with_none(p, PTags.META_INFO_TAG),
                                     DomXmlParser.get_attribute_with_none(p, PTags.TO_ID_TAG),
                                     DomXmlParser.get_attribute_with_none(p, PTags.FB_RX_TAG),
                                     DomXmlParser.get_attribute_with_none(p, PTags.LB_RX_TAG)
                                     ))
    return data_list


def dom_parse_wpr(data):
    wpr_list = data.getElementsByTagName(NetworkElementTags.WPR_TAG.value)
    data_list = []
    for wpr in wpr_list:
        data_list.append(WirelessPacketReception(DomXmlParser.get_attribute_with_none(wpr, WprTags.U_ID_TAG),
                                                 DomXmlParser.get_attribute_with_none(wpr, WprTags.T_ID_TAG),
                                                 DomXmlParser.get_attribute_with_none(wpr, WprTags.FB_RX_TAG),
                                                 DomXmlParser.get_attribute_with_none(wpr, WprTags.LB_RX_TAG)
                                                 ))
    return data_list


def dom_parse_pr(data):
    pr_list = data.getElementsByTagName(NetworkElementTags.PR_TAG.value)
    data_list = []
    for pr in pr_list:
        data_list.append(Broadcaster(DomXmlParser.get_attribute_with_none(pr, PrTags.U_ID_TAG),
                                     DomXmlParser.get_attribute_with_none(pr, PrTags.F_ID_TAG),
                                     DomXmlParser.get_attribute_with_none(pr, PrTags.FB_TX_TAG),
                                     DomXmlParser.get_attribute_with_none(pr, PrTags.META_INFO_TAG)
                                     ))
    return data_list


def dom_parse_res(data):
    res_list = data.getElementsByTagName(NetworkElementTags.RES_TAG.value)
    data_list = []
    for res in res_list:
        data_list.append(Resource(DomXmlParser.get_attribute_with_none(res, ResTags.RID_TAG),
                                  DomXmlParser.get_attribute_with_none(res, ResTags.P_TAG)
                                  ))
    return data_list


def dom_parse_link(data):
    link_list = data.getElementsByTagName(NetworkElementTags.LINK_TAG.value)
    data_list = []
    for link in link_list:
        data_list.append(Link(DomXmlParser.get_attribute_with_none(link, LinkTags.FROM_ID_TAG),
                              DomXmlParser.get_attribute_with_none(link, LinkTags.TO_ID_TAG),
                              DomXmlParser.get_attribute_with_none(link, LinkTags.FD_TAG),
                              DomXmlParser.get_attribute_with_none(link, LinkTags.TD_TAG),
                              DomXmlParser.get_attribute_with_none(link, LinkTags.LD_TAG)
                              ))
    return data_list
