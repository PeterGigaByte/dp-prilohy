from network_elements.tags import NonP2pLinkPropertiesTags

"""<nonp2plinkproperties>"""


class NonP2pLinkProperties:
    def __init__(self, id, ip_address, channel_type):
        self.id = id
        self.ip_address = ip_address
        self.channel_type = channel_type

    def to_dict(self):
        return {
            NonP2pLinkPropertiesTags.ID_TAG.value: self.id,
            NonP2pLinkPropertiesTags.IP_ADDRESS_TAG.value: self.ip_address,
            NonP2pLinkPropertiesTags.CHANNEL_TYPE_TAG.value: self.channel_type
        }
