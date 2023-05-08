from concurrent.futures import ProcessPoolExecutor

from PyQt5.QtCore import QThread
from lxml import etree

from database.database import process_batch, remove_database
from network_elements.elements import (
    Address, Anim, Ip, IpV6, Link, Ncs, Node, NonP2pLinkProperties,
    NodeUpdate, WiredPacket, Broadcaster, Resource, WirelessPacketReception
)
from network_elements.tags import NetworkElementTags, AnimTags, NodeTags, NuTags, NonP2pLinkPropertiesTags, AddressTags, \
    IpTags, IpV6Tags, NcsTags, PTags, WprTags, PrTags, ResTags, LinkTags


def parse_tag(selected_tag):
    match selected_tag.tag:
        case NetworkElementTags.ANIM_TAG.value:
            return Anim(selected_tag.attrib.get(AnimTags.VER_TAG),
                        selected_tag.attrib.get(AnimTags.FILE_TYPE_TAG)
                        )

        case NetworkElementTags.NODE_TAG.value:
            return Node(selected_tag.attrib.get(NodeTags.ID_TAG),
                        selected_tag.attrib.get(NodeTags.SYS_ID_TAG),
                        selected_tag.attrib.get(NodeTags.LOC_X_TAG),
                        selected_tag.attrib.get(NodeTags.LOC_Y_TAG),
                        selected_tag.attrib.get(NodeTags.LOC_Z_TAG)
                        )

        case NetworkElementTags.NU_TAG.value:
            return NodeUpdate(selected_tag.attrib.get(NuTags.P_TAG),
                              selected_tag.attrib.get(NuTags.T_TAG),
                              selected_tag.attrib.get(NuTags.ID_TAG),
                              selected_tag.attrib.get(NuTags.COLOR_R_TAG),
                              selected_tag.attrib.get(NuTags.COLOR_G_TAG),
                              selected_tag.attrib.get(NuTags.COLOR_B_TAG),
                              selected_tag.attrib.get(NuTags.WIDTH_TAG),
                              selected_tag.attrib.get(NuTags.HEIGHT_TAG),
                              selected_tag.attrib.get(NuTags.COORD_X_TAG),
                              selected_tag.attrib.get(NuTags.COORD_Y_TAG),
                              selected_tag.attrib.get(NuTags.COORD_Z_TAG),
                              selected_tag.attrib.get(NuTags.DESCRIPTION_TAG),
                              )

        case NetworkElementTags.NONP2PLINKPROPERTIES_TAG.value:
            return NonP2pLinkProperties(selected_tag.attrib.get(NonP2pLinkPropertiesTags.ID_TAG),
                                        selected_tag.attrib.get(NonP2pLinkPropertiesTags.IP_ADDRESS_TAG),
                                        selected_tag.attrib.get(NonP2pLinkPropertiesTags.CHANNEL_TYPE_TAG)
                                        )
        case NetworkElementTags.IP_TAG.value:
            addresses = selected_tag.findall(NetworkElementTags.ADDRESS_TAG.value)
            addresses_list = []
            for address in addresses:
                addresses_list.append(Address(address.text))
            return Ip(selected_tag.attrib.get(IpTags.N_TAG), addresses_list)

        case NetworkElementTags.IPV6_TAG.value:
            addresses = selected_tag.findall(NetworkElementTags.ADDRESS_TAG.value)
            addresses_list = []
            for _ in addresses:
                addresses_list.append(Address(selected_tag.attrib.get(AddressTags.IP_ADDRESS_TAG)))
            return IpV6(selected_tag.attrib.get(IpV6Tags.N_TAG), addresses_list)

        case NetworkElementTags.ADDRESS_TAG.value:
            return Address(selected_tag.text)

        case NetworkElementTags.NCS_TAG.value:
            return Ncs(selected_tag.attrib.get(NcsTags.NC_ID_TAG),
                       selected_tag.attrib.get(NcsTags.N_TAG),
                       selected_tag.attrib.get(NcsTags.T_TAG)
                       )

        case NetworkElementTags.P_TAG.value:
            return WiredPacket(selected_tag.attrib.get(PTags.FROM_ID_TAG),
                               selected_tag.attrib.get(PTags.FB_TX_TAG),
                               selected_tag.attrib.get(PTags.LB_TX_TAG),
                               selected_tag.attrib.get(PTags.META_INFO_TAG),
                               selected_tag.attrib.get(PTags.TO_ID_TAG),
                               selected_tag.attrib.get(PTags.FB_RX_TAG),
                               selected_tag.attrib.get(PTags.LB_RX_TAG)
                               )

        case NetworkElementTags.WPR_TAG.value:
            return WirelessPacketReception(selected_tag.attrib.get(WprTags.U_ID_TAG),
                                           selected_tag.attrib.get(WprTags.T_ID_TAG),
                                           selected_tag.attrib.get(WprTags.FB_RX_TAG),
                                           selected_tag.attrib.get(WprTags.LB_RX_TAG)
                                           )
        case NetworkElementTags.PR_TAG.value:
            return Broadcaster(selected_tag.attrib.get(PrTags.U_ID_TAG),
                               selected_tag.attrib.get(PrTags.F_ID_TAG),
                               selected_tag.attrib.get(PrTags.FB_TX_TAG),
                               selected_tag.attrib.get(PrTags.META_INFO_TAG)
                               )
        case NetworkElementTags.RES_TAG.value:
            return Resource(selected_tag.attrib.get(ResTags.RID_TAG),
                            selected_tag.attrib.get(ResTags.P_TAG)
                            )
        case NetworkElementTags.LINK_TAG.value:
            return Link(selected_tag.attrib.get(LinkTags.FROM_ID_TAG),
                        selected_tag.attrib.get(LinkTags.TO_ID_TAG),
                        selected_tag.attrib.get(LinkTags.FD_TAG),
                        selected_tag.attrib.get(LinkTags.TD_TAG),
                        selected_tag.attrib.get(LinkTags.LD_TAG)
                        )


class ElementTreeXmlParser(QThread):
    def __init__(self, bottom_dock_widget):
        super().__init__()
        self.batch_size = None
        self.xml_file_path = None
        self.bottom_dock_widget = bottom_dock_widget
        self.anim = None
        self.none_type = None

    def parse(self, xml_file_path, batch_size):
        self.xml_file_path = xml_file_path
        self.batch_size = batch_size
        self.start()

    def run(self):
        remove_database()
        self.bottom_dock_widget.log('Xml treeElement parser begin.')
        self.bottom_dock_widget.log('File path: {0}'.format(self.xml_file_path))

        context = etree.iterparse(self.xml_file_path, events=("start", "end"))
        event, root = next(context)

        self.anim = parse_tag(root)

        self.none_type = 0
        batch = []

        with ProcessPoolExecutor() as executor:
            for event, selected_tag in context:
                if event == "end":
                    item = parse_tag(selected_tag)

                    if item is None:
                        self.none_type += 1
                        print(f'Unknown tag in main content : {item}')
                    else:
                        batch.append(item)

                    if len(batch) >= self.batch_size:
                        executor.submit(process_batch,
                                        batch.copy())  # Submit the batch processing task to the process pool
                        batch = []

                    # Clear the selected_tag and remove it from the tree to save memory
                    selected_tag.clear()
                    while selected_tag.getprevious() is not None:
                        del selected_tag.getparent()[0]

            # Save the remaining batch
            if batch:
                process_batch(batch)

        self.anim = None
        self.bottom_dock_widget.log(f'NoneType tags : {self.none_type}')
        self.bottom_dock_widget.log('Xml TreeElement parser end.')
