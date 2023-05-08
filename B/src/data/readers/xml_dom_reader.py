from xml.dom.minidom import parse

from src.data.objects.objects_definition import Tags, Anim, Node, Nu, NonP2pLinkProperties, Ncs, P, \
    Wpr, Pr, Res, Link, Ip, Address, IpV6


def call_xml_dom_parser(path):
    root = parse(path)

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
    return anim


def dom_parse_anim(data):
    anim_node = data.childNodes[0]
    return Anim(Tags.ANIM_TAG.value,
                anim_node.getAttribute(Anim.VER_TAG),
                anim_node.getAttribute(Anim.FILE_TYPE_TAG)
                )


def dom_parse_node(data):
    nodes = data.getElementsByTagName(Tags.NODE_TAG.value)
    data_list = []
    for node in nodes:
        data_list.append(Node(Tags.NODE_TAG.value,
                              node.getAttribute(Node.ID_TAG),
                              node.getAttribute(Node.SYS_ID_TAG),
                              node.getAttribute(Node.LOC_X_TAG),
                              node.getAttribute(Node.LOC_Y_TAG)
                              ))
    return data_list


def dom_parse_nu(data):
    nus = data.getElementsByTagName(Tags.NU_TAG.value)
    data_list = []
    for nu in nus:
        data_list.append(Nu(Tags.NU_TAG.value,
                            nu.getAttribute(Nu.P_TAG),
                            nu.getAttribute(Nu.T_TAG),
                            nu.getAttribute(Nu.ID_TAG),
                            nu.getAttribute(Nu.COLOR_R_TAG),
                            nu.getAttribute(Nu.COLOR_G_TAG),
                            nu.getAttribute(Nu.COLOR_B_TAG),
                            nu.getAttribute(Nu.WIDTH_TAG),
                            nu.getAttribute(Nu.HEIGHT_TAG),
                            nu.getAttribute(Nu.COORD_X_TAG),
                            nu.getAttribute(Nu.COORD_Y_TAG),
                            nu.getAttribute(Nu.DESCRIPTION_TAG),
                            ))
    return data_list


def dom_parse_non_link_properties(data):
    non_link_properties_list = data.getElementsByTagName(Tags.NONP2PLINKPROPERTIES_TAG.value)
    data_list = []
    for non_link_property in non_link_properties_list:
        data_list.append(NonP2pLinkProperties(Tags.NONP2PLINKPROPERTIES_TAG.value,
                                              non_link_property.getAttribute(NonP2pLinkProperties.ID_TAG),
                                              non_link_property.getAttribute(NonP2pLinkProperties.IP_ADDRESS_TAG),
                                              non_link_property.getAttribute(NonP2pLinkProperties.CHANNEL_TYPE_TAG)
                                              ))
    return data_list


def dom_parse_ip(data):
    ip_list = data.getElementsByTagName(Tags.IP_TAG.value)
    data_list = []
    for ip in ip_list:
        data_list.append(Ip(Tags.IP_TAG.value,
                            ip.getAttribute(Ip.N_TAG),
                            dom_parse_address(ip)
                            ))
    return data_list


def dom_parse_ipv(data):
    ipv_list = data.getElementsByTagName(Tags.IPV6_TAG.value)
    data_list = []
    for ipv in ipv_list:
        data_list.append(IpV6(Tags.IPV6_TAG.value,
                              ipv.getAttribute(IpV6.N_TAG),
                              dom_parse_address(ipv)
                              ))
    return data_list


def dom_parse_address(data):
    address_list = data.getElementsByTagName(Tags.ADDRESS_TAG.value)
    data_list = []
    for address in address_list:
        data_list.append(Address(Tags.ADDRESS_TAG.value,
                                 address.childNodes[0].nodeValue,
                                 ))
    return data_list


def dom_parse_nsc(data):
    nsc_list = data.getElementsByTagName(Tags.NCS_TAG.value)
    data_list = []
    for nsc in nsc_list:
        data_list.append(Ncs(Tags.NCS_TAG.value,
                             nsc.getAttribute(Ncs.NC_ID_TAG),
                             nsc.getAttribute(Ncs.N_TAG),
                             nsc.getAttribute(Ncs.T_TAG)
                             ))
    return data_list


def dom_parse_p(data):
    p_list = data.getElementsByTagName(Tags.P_TAG.value)
    data_list = []
    for p in p_list:
        data_list.append(P(Tags.P_TAG.value,
                           p.getAttribute(P.FROM_ID_TAG),
                           p.getAttribute(P.FB_TX_TAG),
                           p.getAttribute(P.META_INFO_TAG),
                           p.getAttribute(P.TO_ID_TAG),
                           p.getAttribute(P.FB_RX_TAG),
                           p.getAttribute(P.LB_RX_TAG)
                           ))
    return data_list


def dom_parse_wpr(data):
    wpr_list = data.getElementsByTagName(Tags.WPR_TAG.value)
    data_list = []
    for wpr in wpr_list:
        data_list.append(Wpr(Tags.WPR_TAG.value,
                             wpr.getAttribute(Wpr.U_ID_TAG),
                             wpr.getAttribute(Wpr.T_ID_TAG),
                             wpr.getAttribute(Wpr.FB_RX_TAG),
                             wpr.getAttribute(Wpr.LB_RX_TAG)
                             ))
    return data_list


def dom_parse_pr(data):
    pr_list = data.getElementsByTagName(Tags.PR_TAG.value)
    data_list = []
    for pr in pr_list:
        data_list.append(Pr(Tags.PR_TAG,
                            pr.getAttribute(Pr.U_ID_TAG),
                            pr.getAttribute(Pr.F_ID_TAG),
                            pr.getAttribute(Pr.FB_TX_TAG),
                            pr.getAttribute(Pr.META_INFO_TAG)
                            ))
    return data_list


def dom_parse_res(data):
    res_list = data.getElementsByTagName(Tags.RES_TAG.value)
    data_list = []
    for res in res_list:
        data_list.append(Res(Tags.RES_TAG.value,
                             res.getAttribute(Res.RID_TAG),
                             res.getAttribute(Res.P_TAG)
                             ))
    return data_list


def dom_parse_link(data):
    link_list = data.getElementsByTagName(Tags.LINK_TAG.value)
    data_list = []
    for link in link_list:
        data_list.append(Link(Tags.LINK_TAG.value,
                              link.getAttribute(Link.FROM_ID_TAG),
                              link.getAttribute(Link.TO_ID_TAG),
                              link.getAttribute(Link.FD_TAG),
                              link.getAttribute(Link.TD_TAG),
                              link.getAttribute(Link.LD_TAG)
                              ))
    return data_list
