from network_elements.tags import LinkTags

"""<link>"""


class Link:
    def __init__(self, from_id, to_id, fd, td, ld):
        self.from_id = from_id
        self.to_id = to_id
        self.fd = fd
        self.td = td
        self.ld = ld

    def to_dict(self):
        return {
            LinkTags.FROM_ID_TAG.value: self.from_id,
            LinkTags.TO_ID_TAG.value: self.to_id,
            LinkTags.FD_TAG.value: self.fd,
            LinkTags.TD_TAG.value: self.td,
            LinkTags.LD_TAG.value: self.ld
        }
