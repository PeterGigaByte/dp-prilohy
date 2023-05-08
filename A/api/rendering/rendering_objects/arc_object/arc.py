import uuid

import numpy as np
import vtk

from utils.renderingUtils import normalize_rgb


class Arc:
    def __init__(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        self.packet_id = packet_id if packet_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.actor = self.create_actor()

    def create_actor(self):
        wifi_assembly = vtk.vtkAssembly()

        # Increase this factor to scale the size of the WiFi signal
        scale_factor = 10

        for i in range(1, 4):
            arc = vtk.vtkArcSource()
            arc.SetPolarVector(i * self.size * scale_factor, 0, 0)
            arc.SetAngle(120)
            arc.SetResolution(50)

            arc_mapper = vtk.vtkPolyDataMapper()
            arc_mapper.SetInputConnection(arc.GetOutputPort())

            arc_actor = vtk.vtkActor()
            arc_actor.SetMapper(arc_mapper)
            arc_actor.GetProperty().SetColor(*normalize_rgb(self.color))
            arc_actor.RotateZ(30)
            arc_actor.RotateY(-90)

            wifi_assembly.AddPart(arc_actor)

        wifi_assembly.SetPosition(self.x, self.y, self.z)
        wifi_assembly.SetScale(scale_factor)

        return wifi_assembly

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.actor)

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.actor.SetPosition(self.x, self.y, self.z)
