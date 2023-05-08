from network_elements.tags import ResTags

"""<res>"""


class Resource:
    def __init__(self, rid, p):
        self.rid = rid
        self.p = p

    def to_dict(self):
        return {
            ResTags.RID_TAG.value: self.rid,
            ResTags.P_TAG.value: self.p
        }
