from network_elements.tags import PrTags

"""<pr>"""


class Broadcaster:
    def __init__(self, u_id, f_id, first_byte_transmission_time, meta_info):
        self.unique_id = u_id
        self.from_id = f_id
        self.first_byte_transmission_time = first_byte_transmission_time
        self.meta_info = meta_info

    def to_dict(self):
        return {
            PrTags.U_ID_TAG.value: self.unique_id,
            PrTags.F_ID_TAG.value: self.from_id,
            PrTags.FB_TX_TAG.value: self.first_byte_transmission_time,
            PrTags.META_INFO_TAG.value: self.meta_info
        }
