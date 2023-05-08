# Python program to read
# json file


import json

from src.data.objects.objects_definition import Tags, Anim, Node, Nu, NonP2pLinkProperties, P, \
    Wpr, Ip, Pr, Res, Link, Ncs, Address, IpV6

prefix = '@'


def call_json_parser(path):
    # Opening JSON file
    f = open(path)

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    data = data[Tags.ANIM_TAG.value]
    # Iterating through the json
    # list
    # for i in data['emp_details']:
    #     print(i)
    anim = Anim(Tags.ANIM_TAG.value,
                data.get(prefix + Anim.VER_TAG),
                data.get(prefix + Anim.FILE_TYPE_TAG)
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
    return anim


def json_parse_nodes(data):
    data_list = []
    for node in data.get(Tags.NODE_TAG.value) or []:
        data_list.append(Node(Tags.NODE_TAG.value,
                              node.get(prefix + Node.ID_TAG),
                              node.get(prefix + Node.SYS_ID_TAG),
                              node.get(prefix + Node.LOC_X_TAG),
                              node.get(prefix + Node.LOC_Y_TAG)
                              ))
    return data_list


def json_parse_nu(data):
    data_list = []
    for nu in data.get(Tags.NU_TAG.value) or []:
        data_list.append(Nu(Tags.NU_TAG.value,
                            nu.get(prefix + Nu.P_TAG),
                            nu.get(prefix + Nu.T_TAG),
                            nu.get(prefix + Nu.ID_TAG),
                            nu.get(prefix + Nu.COLOR_R_TAG),
                            nu.get(prefix + Nu.COLOR_G_TAG),
                            nu.get(prefix + Nu.COLOR_B_TAG),
                            nu.get(prefix + Nu.WIDTH_TAG),
                            nu.get(prefix + Nu.HEIGHT_TAG),
                            nu.get(prefix + Nu.COORD_X_TAG),
                            nu.get(prefix + Nu.COORD_Y_TAG),
                            nu.get(prefix + Nu.DESCRIPTION_TAG)
                            ))
    return data_list


def json_parse_non_link_properties(data):
    data_list = []
    for non_link_property in data.get(Tags.NONP2PLINKPROPERTIES_TAG.value) or []:
        data_list.append(NonP2pLinkProperties(Tags.NONP2PLINKPROPERTIES_TAG.value,
                                              non_link_property.get(prefix + NonP2pLinkProperties.ID_TAG),
                                              non_link_property.get(prefix + NonP2pLinkProperties.IP_ADDRESS_TAG),
                                              non_link_property.get(prefix + NonP2pLinkProperties.CHANNEL_TYPE_TAG)
                                              ))
    return data_list


def json_parse_ip(data):
    data_list = []
    for ip in data.get(Tags.IP_TAG.value) or []:
        data_list.append(Ip(Tags.IP_TAG.value,
                            ip.get(prefix + Ip.N_TAG),
                            json_parse_address(ip.get(Tags.ADDRESS_TAG.value))
                            ))
    return data_list


def json_parse_ipv(data):
    data_list = []
    for ipv in data.get(Tags.IPV6_TAG.value) or []:
        data_list.append(IpV6(Tags.IPV6_TAG.value,
                              ipv.get(prefix + IpV6.N_TAG),
                              json_parse_address(ipv.get(Tags.ADDRESS_TAG.value))
                              ))
    return data_list


def json_parse_p(data):
    data_list = []
    for p in data.get(Tags.P_TAG.value) or []:
        data_list.append(P(Tags.P_TAG.value,
                           p.get(prefix + P.FROM_ID_TAG),
                           p.get(prefix + P.FB_TX_TAG),
                           p.get(prefix + P.META_INFO_TAG),
                           p.get(prefix + P.TO_ID_TAG),
                           p.get(prefix + P.FB_RX_TAG),
                           p.get(prefix + P.LB_RX_TAG)
                           ))
    return data_list


def json_parse_wpr(data):
    data_list = []
    for wpr in data.get(Tags.WPR_TAG.value) or []:
        data_list.append(Wpr(Tags.WPR_TAG.value,
                             wpr.get(prefix + Wpr.U_ID_TAG),
                             wpr.get(prefix + Wpr.T_ID_TAG),
                             wpr.get(prefix + Wpr.FB_RX_TAG),
                             wpr.get(prefix + Wpr.LB_RX_TAG)
                             ))
    return data_list


def json_parse_pr(data):
    data_list = []
    for pr in data.get(Tags.PR_TAG.value) or []:
        data_list.append(Pr(Tags.PR_TAG,
                            pr.get(prefix + Pr.U_ID_TAG),
                            pr.get(prefix + Pr.F_ID_TAG),
                            pr.get(prefix + Pr.FB_TX_TAG),
                            pr.get(prefix + Pr.META_INFO_TAG)
                            ))
    return data_list


def json_parse_res(data):
    data_list = []
    for res in data.get(Tags.RES_TAG.value) or []:
        data_list.append(Res(Tags.RES_TAG,
                             res.get(prefix + Res.RID_TAG),
                             res.get(prefix + Res.P_TAG),
                             ))
    return data_list


def json_parse_link(data):
    data_list = []
    data = data.get(Tags.LINK_TAG.value)
    if data is not None:
        data_list.append(Link(Tags.LINK_TAG.value,
                              data.get(prefix + Link.FROM_ID_TAG),
                              data.get(prefix + Link.TO_ID_TAG),
                              data.get(prefix + Link.FD_TAG),
                              data.get(prefix + Link.TD_TAG),
                              data.get(prefix + Link.LD_TAG)
                              ))
    return data_list


def json_parse_nsc(data):
    data_list = []
    data_list.append(Ncs(Tags.NCS_TAG.value,
                         data.get(Tags.NCS_TAG.value).get(prefix + Ncs.NC_ID_TAG),
                         data.get(Tags.NCS_TAG.value).get(prefix + Ncs.N_TAG),
                         data.get(Tags.NCS_TAG.value).get(prefix + Ncs.T_TAG)
                         ))
    return data_list


def json_parse_address(data):
    data_list = []
    for address in data or []:
        data_list.append(Address(Tags.ADDRESS_TAG.value,
                                 address
                                 ))
    return data_list
