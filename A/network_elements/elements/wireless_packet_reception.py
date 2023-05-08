from network_elements.tags import WprTags

"""<wpr>"""


class WirelessPacketReception:
    def __init__(self, unique_id, to_id, first_byte_received_time, last_byte_received_time, first_byte_transmission_time=None, from_id=None, meta_info=None):
        self.unique_id = unique_id
        self.to_id = to_id
        self.first_byte_received_time = first_byte_received_time
        self.last_byte_received_time = last_byte_received_time
        self.first_byte_transmission_time = first_byte_transmission_time
        self.from_id = from_id
        self.meta_info = meta_info

    def to_dict(self):
        return {
            WprTags.U_ID_TAG.value: self.unique_id,
            WprTags.T_ID_TAG.value: self.to_id,
            WprTags.FB_RX_TAG.value: self.first_byte_received_time,
            WprTags.LB_RX_TAG.value: self.last_byte_received_time
        }
