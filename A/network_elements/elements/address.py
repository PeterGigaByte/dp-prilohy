from network_elements.tags import AddressTags

"""<address>"""


class Address:
    def __init__(self, address):
        self.address = address

    def to_dict(self):
        return {
            AddressTags.IP_ADDRESS_TAG.value: self.address
        }
