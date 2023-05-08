import vtk
from PyQt5.QtCore import Qt
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from utils.calcUtils import calculate_focal_points_xyz, calculate_focal_points_xy


class KeyPressInteractor(QVTKRenderWindowInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if self.GetInteractorStyle() is not None:
            self.GetInteractorStyle().OnKeyPress(event)
            self.GetInteractorStyle().OnKeyRelease()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setFocus()


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self):
        super().__init__()

    def OnKeyPress(self, event):
        event_key = event.key()
        camera = self.GetCurrentRenderer().GetActiveCamera()
        position = list(camera.GetPosition())
        focal_point = list(camera.GetFocalPoint())

        move_speed = 10
        rotation_speed = 10

        update_camera_position = True

        # Get the direction of the camera
        direction = [focal_point[i] - position[i] for i in range(3)]
        x_direction = direction[0]
        y_direction = direction[1]

        # Normalize the direction vector
        direction_magnitude = (x_direction ** 2 + y_direction ** 2) ** 0.5
        x_direction /= direction_magnitude
        y_direction /= direction_magnitude

        match event_key:
            case Qt.Key_W:
                # Move camera forward
                position[0] += move_speed * x_direction
                position[1] += move_speed * y_direction
                focal_point[0] += move_speed * x_direction
                focal_point[1] += move_speed * y_direction
            case Qt.Key_S:
                # Move camera back
                position[0] -= move_speed * x_direction
                position[1] -= move_speed * y_direction
                focal_point[0] -= move_speed * x_direction
                focal_point[1] -= move_speed * y_direction
            case Qt.Key_D:
                # Move camera to the right
                position[0] += move_speed * y_direction
                position[1] -= move_speed * x_direction
                focal_point[0] += move_speed * y_direction
                focal_point[1] -= move_speed * x_direction
            case Qt.Key_A:
                # Move camera to the left
                position[0] -= move_speed * y_direction
                position[1] += move_speed * x_direction
                focal_point[0] -= move_speed * y_direction
                focal_point[1] += move_speed * x_direction
            case Qt.Key_Q:
                # Rotate camera to the left xyz
                camera.Roll(-rotation_speed)
            case Qt.Key_E:
                # Rotate camera to the right xyz
                camera.Roll(rotation_speed)
            case Qt.Key_Right:
                # Rotate camera to the right
                focal_point[0], focal_point[1] = calculate_focal_points_xy(focal_point, position, -10)
            case Qt.Key_Left:
                # Rotate camera to the right
                focal_point[0], focal_point[1] = calculate_focal_points_xy(focal_point, position, 10)
            case Qt.Key_Up:
                # Rotate camera up
                focal_point[0], focal_point[1], focal_point[2] = calculate_focal_points_xyz(focal_point, position, 10)
            case Qt.Key_Down:
                # Rotate camera down
                focal_point[0], focal_point[1], focal_point[2] = calculate_focal_points_xyz(focal_point, position, -10)
            case Qt.Key_U:
                # Move camera up
                position[2] += move_speed
                focal_point[2] += move_speed
            case Qt.Key_I:
                # Move camera down
                position[2] -= move_speed
                focal_point[2] -= move_speed
            case Qt.Key_R:
                # Move camera position
                camera.SetPosition(0, -500, 200)
                camera.SetFocalPoint(0, 0, 0)
                camera.SetViewUp(0, 0, 1)
                camera.SetClippingRange(1, 1000)
                update_camera_position = False

        if update_camera_position:
            camera.SetPosition(position)
            camera.SetFocalPoint(focal_point)

        self.GetCurrentRenderer().ResetCameraClippingRange()

        self.OnMouseMove()
        self.GetInteractor().GetRenderWindow().Render()

    def OnKeyRelease(self):
        pass
