from network_elements.tags import IpV6Tags

"""<ipv6>"""


class IpV6:
    def __init__(self, n, addresses):
        self.n = n
        self.addresses = addresses

    def to_dict(self):
        return {
            IpV6Tags.N_TAG.value: self.n
        }
