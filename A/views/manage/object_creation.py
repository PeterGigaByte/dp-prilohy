def create_node(environment, inputs):
    try:
        x, y, z = [int(inputs[key].text()) for key in ('x', 'y', 'z')]
        environment.vtk_api.create_node(x=x, y=y, z=z)
        environment.bottom_dock_widget.log(f"Node with coordinates [{x},{y},{z}] was created.")
    except ValueError as ve:
        environment.bottom_dock_widget.log(f"Value error was thrown because of wrong arguments for creation of "
                                           f"Node. \n Error: {ve}")


def create_building(environment, inputs):
    try:
        x, y, z = [int(inputs[key].text()) for key in ('x', 'y', 'z')]
        width, height = [int(inputs[key].text()) for key in ('width', 'height')]
        environment.vtk_api.create_building(x, y, z, width, height)
        environment.bottom_dock_widget.log(
            f"Building with coordinates [{x},{y},{z}] was created with width {width} and height {height}.")
    except ValueError as ve:
        environment.bottom_dock_widget.log(f"Value error was thrown because of wrong arguments for creation of Building."
                                           f" \n Error: {ve}")


def create_arrow(environment, inputs):
    try:
        x1, y1, z1, x2, y2, z2 = [int(inputs[key].text()) for key in ('x1', 'y1', 'z1', 'x2', 'y2', 'z2')]
        environment.vtk_api.create_arrow(start=(x1, y1, z1), end=(x2, y2, z2))
        environment.bottom_dock_widget.log(
            f"Arrow from start point  with coordinates [{x1},{y1},{z1}] was created and it is aiming to [{x2}, {y2}, {z2}].")
    except ValueError as ve:
        environment.bottom_dock_widget.log(f"Value error was thrown because of wrong arguments for creation of Arrow."
                                           f" \n Error: {ve}")
