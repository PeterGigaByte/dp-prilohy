import logging
from xml.etree import ElementTree

from src.data.objects.objects_definition import Tags, Anim, Node, Nu, NonP2pLinkProperties, Address, Ip, IpV6, Ncs, P, \
    Wpr, Pr, Res, Link


def tree_element_parse_tag(selected_tag):
    match selected_tag.tag:
        case Tags.ANIM_TAG.value:
            return Anim(selected_tag.tag,
                        selected_tag.attrib.get(Anim.VER_TAG),
                        selected_tag.attrib.get(Anim.FILE_TYPE_TAG)
                        )

        case Tags.NODE_TAG.value:
            return Node(selected_tag.tag,
                        selected_tag.attrib.get(Node.ID_TAG),
                        selected_tag.attrib.get(Node.SYS_ID_TAG),
                        selected_tag.attrib.get(Node.LOC_X_TAG),
                        selected_tag.attrib.get(Node.LOC_Y_TAG)
                        )

        case Tags.NU_TAG.value:
            return Nu(selected_tag.tag,
                      selected_tag.attrib.get(Nu.P_TAG),
                      selected_tag.attrib.get(Nu.T_TAG),
                      selected_tag.attrib.get(Nu.ID_TAG),
                      selected_tag.attrib.get(Nu.COLOR_R_TAG),
                      selected_tag.attrib.get(Nu.COLOR_G_TAG),
                      selected_tag.attrib.get(Nu.COLOR_B_TAG),
                      selected_tag.attrib.get(Nu.WIDTH_TAG),
                      selected_tag.attrib.get(Nu.HEIGHT_TAG),
                      selected_tag.attrib.get(Nu.COORD_X_TAG),
                      selected_tag.attrib.get(Nu.COORD_Y_TAG),
                      selected_tag.attrib.get(Nu.DESCRIPTION_TAG),
                      )

        case Tags.NONP2PLINKPROPERTIES_TAG.value:
            return NonP2pLinkProperties(selected_tag.tag,
                                        selected_tag.attrib.get(NonP2pLinkProperties.ID_TAG),
                                        selected_tag.attrib.get(NonP2pLinkProperties.IP_ADDRESS_TAG),
                                        selected_tag.attrib.get(NonP2pLinkProperties.CHANNEL_TYPE_TAG)
                                        )
        case Tags.IP_TAG.value:
            addresses = selected_tag.findall(Tags.ADDRESS_TAG.value)
            addresses_list = []
            for address in addresses:
                addresses_list.append(Address(address.tag, selected_tag.attrib.get(Address.IP_ADDRESS_TAG)))
            return Ip(selected_tag.tag, selected_tag.attrib.get(Ip.N_TAG), addresses_list)

        case Tags.IPV6_TAG.value:
            addresses = selected_tag.findall(Tags.ADDRESS_TAG.value)
            addresses_list = []
            for address in addresses:
                addresses_list.append(Address(address.tag, selected_tag.attrib.get(Address.IP_ADDRESS_TAG)))
            return IpV6(selected_tag.tag, selected_tag.attrib.get(IpV6.N_TAG), addresses_list)

        case Tags.ADDRESS_TAG.value:
            return Address(selected_tag.tag, selected_tag.attrib.get(Address.IP_ADDRESS_TAG))

        case Tags.NCS_TAG.value:
            return Ncs(selected_tag.tag,
                       selected_tag.attrib.get(Ncs.NC_ID_TAG),
                       selected_tag.attrib.get(Ncs.N_TAG),
                       selected_tag.attrib.get(Ncs.T_TAG)
                       )

        case Tags.P_TAG.value:
            return P(selected_tag.tag,
                     selected_tag.attrib.get(P.FROM_ID_TAG),
                     selected_tag.attrib.get(P.FB_TX_TAG),
                     selected_tag.attrib.get(P.META_INFO_TAG),
                     selected_tag.attrib.get(P.TO_ID_TAG),
                     selected_tag.attrib.get(P.FB_RX_TAG),
                     selected_tag.attrib.get(P.LB_RX_TAG)
                     )

        case Tags.WPR_TAG.value:
            return Wpr(selected_tag.tag,
                       selected_tag.attrib.get(Wpr.U_ID_TAG),
                       selected_tag.attrib.get(Wpr.T_ID_TAG),
                       selected_tag.attrib.get(Wpr.FB_RX_TAG),
                       selected_tag.attrib.get(Wpr.LB_RX_TAG)
                       )
        case Tags.PR_TAG.value:
            return Pr(selected_tag.tag,
                      selected_tag.attrib.get(Pr.U_ID_TAG),
                      selected_tag.attrib.get(Pr.F_ID_TAG),
                      selected_tag.attrib.get(Pr.FB_TX_TAG),
                      selected_tag.attrib.get(Pr.META_INFO_TAG)
                      )
        case Tags.RES_TAG.value:
            return Res(selected_tag.tag,
                       selected_tag.attrib.get(Res.RID_TAG),
                       selected_tag.attrib.get(Res.P_TAG)
                       )
        case Tags.LINK_TAG.value:
            return Link(selected_tag.tag,
                        selected_tag.attrib.get(Link.FROM_ID_TAG),
                        selected_tag.attrib.get(Link.TO_ID_TAG),
                        selected_tag.attrib.get(Link.FD_TAG),
                        selected_tag.attrib.get(Link.TD_TAG),
                        selected_tag.attrib.get(Link.LD_TAG)
                        )


def call_xml_tree_element_parser(path):
    logging.debug('Xml parser begin')
    logging.debug('File path: {0}'.format(path))
    path = path
    tree = ElementTree.parse(path)
    tags = tree.getroot()

    # anim tag
    anim = tree_element_parse_tag(tags)
    anim_content = []

    # none_type counter
    none_type = 0

    # read all tags
    for selected_tag in tags:
        item = tree_element_parse_tag(selected_tag)

        # check if some item has no type - test functionality
        if item is None:
            none_type += 1
            print(f'Unknown tag in main content : {item}')
        anim_content.append(tree_element_parse_tag(selected_tag))

    # add to anim object as content
    anim.content = anim_content

    # info print
    print(f'NoneType tags : {none_type}')
    logging.debug('Xml parser end')
    return anim, none_type
