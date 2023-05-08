from network_elements.tags import NodeTags

"""<node_object>"""


class Node:
    def __init__(self, id, sys_id, loc_x, loc_y, loc_z=0):
        self.id = id
        self.sys_id = sys_id
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.loc_z = loc_z if loc_z is not None else 0

    def to_dict(self):
        return {
            NodeTags.ID_TAG.value: self.id,
            NodeTags.SYS_ID_TAG.value: self.sys_id,
            NodeTags.LOC_X_TAG.value: self.loc_x,
            NodeTags.LOC_Y_TAG.value: self.loc_y,
            NodeTags.LOC_Z_TAG.value: self.loc_z
        }

    def set_coordinates(self, x, y, z):
        self.loc_x = x
        self.loc_y = y
        self.loc_z = z


