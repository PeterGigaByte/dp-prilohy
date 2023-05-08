import uuid

import vtk

from utils.renderingUtils import normalize_rgb


class AlternativeWirelessPacket:
    def __init__(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        self.packet_id = packet_id if packet_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.actor = self.create_actor()

    def create_actor(self):
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetRadius(self.size)
        cylinder.SetHeight(self.size * 2.5)
        cylinder.SetResolution(32)

        cylinder_mapper = vtk.vtkPolyDataMapper()
        cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

        cylinder_actor = vtk.vtkActor()
        cylinder_actor.SetMapper(cylinder_mapper)
        cylinder_actor.GetProperty().SetColor(*normalize_rgb(self.color))
        cylinder_actor.SetPosition(self.x, self.y, self.z)

        return cylinder_actor

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.actor)

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.actor.SetPosition(self.x, self.y, self.z)
