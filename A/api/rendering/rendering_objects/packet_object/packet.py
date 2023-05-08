import uuid

import vtk

from utils.renderingUtils import normalize_rgb


class Packet:
    def __init__(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        self.packet_id = packet_id if packet_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.actor = self.create_actor()

    def create_actor(self):
        cube = vtk.vtkCubeSource()
        cube.SetXLength(self.size)
        cube.SetYLength(self.size)
        cube.SetZLength(self.size)

        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(cube_mapper)
        cube_actor.GetProperty().SetColor(*normalize_rgb(self.color))

        cube_actor.SetPosition(self.x, self.y, self.z)

        return cube_actor

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.actor)

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.actor.SetPosition(self.x, self.y, self.z)