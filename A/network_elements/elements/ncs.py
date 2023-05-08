from network_elements.tags import NcsTags

"""<ncs>"""


class Ncs:
    def __init__(self, nc_id, n, t):
        self.nc_id = nc_id
        self.n = n
        self.t = t

    def to_dict(self):
        return {
            NcsTags.NC_ID_TAG.value: self.nc_id,
            NcsTags.N_TAG.value: self.n,
            NcsTags.T_TAG.value: self.t
        }
