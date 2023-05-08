import uuid

import vtk


class Building:
    def __init__(self, x, y, z, width, height, cube_color=(0.5, 0.5, 0.5), building_id=None):
        self.building_id = building_id if building_id else uuid.uuid4()
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.cube_color = cube_color
        self.building_actor = self.create_actor()

    def create_actor(self):
        """Create a building_object at the specified location."""
        cube = vtk.vtkCubeSource()
        cube.SetXLength(self.width)
        cube.SetYLength(self.width)
        cube.SetZLength(self.height)
        cube.SetCenter(self.x, self.y, self.z + self.height / 2)

        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube.GetOutputPort())

        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(cube_mapper)
        cube_actor.GetProperty().SetColor(0.5, 0.5, 0.5)

        return cube_actor

    def add_to_renderer(self, renderer):
        renderer.AddActor(self.building_actor)

    def remove_from_renderer(self, renderer):
        renderer.RemoveActor(self.building_actor)

    def update_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.building_actor.SetPosition(self.x, self.y, self.z)