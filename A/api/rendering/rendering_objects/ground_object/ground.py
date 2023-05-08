import uuid

import vtk


class Ground:
    def __init__(self, resolution, origin, point1, point2, color=(0, 0, 255), ground_id=None):
        self.ground_id = ground_id if ground_id else uuid.uuid4()
        self.resolution = resolution
        self.origin = origin
        self.point1 = point1
        self.point2 = point2
        self.color = color
        self.actor = self.create_actor()

    def create_actor(self):
        """Create a ground_object plane for the environment."""
        plane = vtk.vtkPlaneSource()
        plane.SetResolution(self.resolution[0], self.resolution[1])
        plane.SetOrigin(self.origin[0], self.origin[1], self.origin[2])
        plane.SetPoint1(self.point1[0], self.point1[1], self.point1[2])
        plane.SetPoint2(self.point2[0], self.point2[1], self.point2[2])

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        ground_actor = vtk.vtkActor()
        ground_actor.SetMapper(mapper)
        ground_actor.GetProperty().SetColor(self.color[0], self.color[1], self.color[2])

        return ground_actor

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.actor)

    def move_ground(self, step_size, renderer):
        """Move the ground_object up or down by a specified step size."""
        renderer.RemoveActor(self.actor)
        self.origin = (self.origin[0], self.origin[1], self.origin[2] + step_size)
        self.point1 = (self.point1[0], self.point1[1], self.point1[2] + step_size)
        self.point2 = (self.point2[0], self.point2[1], self.point2[2] + step_size)
        self.actor = self.create_actor()
        self.add_to_renderer(renderer)
        renderer.GetRenderWindow().GetInteractor().Render()
