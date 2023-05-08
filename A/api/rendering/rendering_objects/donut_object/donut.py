import uuid

import numpy as np
import vtk

from utils.renderingUtils import normalize_rgb


class Donut:
    def __init__(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        self.packet_id = packet_id if packet_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.actor = self.create_actor()

    def create_actor(self):
        # Create a torus for the base object
        torus = vtk.vtkParametricTorus()
        torus.SetRingRadius(self.size * 0.5)
        torus.SetCrossSectionRadius(self.size * 0.25)

        torus_source = vtk.vtkParametricFunctionSource()
        torus_source.SetParametricFunction(torus)
        torus_source.SetScalarModeToZ()

        torus_mapper = vtk.vtkPolyDataMapper()
        torus_mapper.SetInputConnection(torus_source.GetOutputPort())

        torus_actor = vtk.vtkActor()
        torus_actor.SetMapper(torus_mapper)
        torus_actor.GetProperty().SetColor(*normalize_rgb(self.color))

        torus_actor.SetPosition(self.x, self.y, self.z)

        return torus_actor

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.actor)

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.actor.SetPosition(self.x, self.y, self.z)
