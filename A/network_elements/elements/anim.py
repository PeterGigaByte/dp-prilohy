from network_elements.tags import AnimTags

"""<anim>"""


class Anim:
    def __init__(self, ver, file_type):
        self.ver = ver
        self.file_type = file_type

    def to_dict(self):
        return {
            AnimTags.VER_TAG.value: self.ver,
            AnimTags.FILE_TYPE_TAG.value: self.file_type
        }
