import uuid

import numpy as np
import vtk

from utils.renderingUtils import normalize_rgb


class Human:
    def __init__(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        self.packet_id = packet_id if packet_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.color = color
        self.actor = self.create_actor()

    def create_actor(self):
        # Create legs
        leg_length = self.size * 2.5
        num_legs = 3

        legs_assembly = vtk.vtkAssembly()

        for i in range(num_legs):
            angle = 2 * np.pi * i / num_legs
            leg_start = (self.x + self.size * np.cos(angle), self.y + self.size * np.sin(angle), self.z)
            leg_end = (self.x, self.y, self.z + leg_length)

            leg = vtk.vtkLineSource()
            leg.SetPoint1(*leg_start)
            leg.SetPoint2(*leg_end)

            leg_mapper = vtk.vtkPolyDataMapper()
            leg_mapper.SetInputConnection(leg.GetOutputPort())

            leg_actor = vtk.vtkActor()
            leg_actor.SetMapper(leg_mapper)
            leg_actor.GetProperty().SetColor(*normalize_rgb(self.color))

            legs_assembly.AddPart(leg_actor)

        # Create a sphere for the top
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(self.size)
        sphere.SetThetaResolution(32)
        sphere.SetPhiResolution(32)

        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere.GetOutputPort())

        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(*normalize_rgb(self.color))

        sphere_actor.SetPosition(self.x, self.y, self.z + leg_length)

        # Combine legs and sphere
        assembly = vtk.vtkAssembly()
        assembly.AddPart(legs_assembly)
        assembly.AddPart(sphere_actor)

        return assembly

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.actor)

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.actor.SetPosition(self.x, self.y, self.z)
