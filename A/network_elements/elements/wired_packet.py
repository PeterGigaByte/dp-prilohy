from network_elements.tags import PTags

"""<p>"""


class WiredPacket:
    def __init__(self, from_id, first_byte_transmission_time, last_byte_transmission_time, meta_info, to_id, first_byte_received_time, last_byte_received_time):
        self.from_id = from_id
        self.first_byte_transmission_time = first_byte_transmission_time
        self.last_byte_transmission_time = last_byte_transmission_time
        self.meta_info = meta_info
        self.to_id = to_id
        self.first_byte_received_time = first_byte_received_time
        self.last_byte_received_time = last_byte_received_time

    def to_dict(self):
        return {
            PTags.FROM_ID_TAG.value: self.from_id,
            PTags.FB_TX_TAG.value: self.first_byte_transmission_time,
            PTags.LB_TX_TAG.value: self.last_byte_transmission_time,
            PTags.META_INFO_TAG.value: self.meta_info,
            PTags.TO_ID_TAG.value: self.to_id,
            PTags.FB_RX_TAG.value: self.first_byte_received_time,
            PTags.LB_RX_TAG.value: self.last_byte_received_time
        }
