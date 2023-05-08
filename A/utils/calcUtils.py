import math

import numpy as np


def calculate_focal_points_xy(focal_point, position, angle):
    # Rotate camera to the right
    dx = focal_point[0] - position[0]
    dy = focal_point[1] - position[1]

    new_dx = dx * math.cos(math.radians(angle)) - dy * math.sin(math.radians(angle))
    new_dy = dx * math.sin(math.radians(angle)) + dy * math.cos(math.radians(angle))

    focal_point[0] = position[0] + new_dx
    focal_point[1] = position[1] + new_dy
    return focal_point[0], focal_point[1]


def calculate_focal_points_xyz(focal_point, position, angle):
    # Rotate camera up or down
    dx = focal_point[0] - position[0]
    dy = focal_point[1] - position[1]
    dz = focal_point[2] - position[2]

    # Calculate the horizontal distance
    hor_dist = math.sqrt(dx ** 2 + dy ** 2)

    # Calculate the ÁM current inclination angle
    inclination = math.atan2(dz, hor_dist)

    # Update the inclination angle
    new_inclination = inclination + math.radians(angle)
    new_inclination = max(min(new_inclination, math.pi / 2 - 0.01), -math.pi / 2 + 0.01)

    # Calculate the new vertical (z) distance
    new_dz = hor_dist * math.tan(new_inclination)

    # Update the focal point
    focal_point[2] = position[2] + new_dz

    return focal_point[0], focal_point[1], focal_point[2]


def interpolate_coordinates_3D(src_coord, dst_coord, step, num_steps):
    x_src, y_src, z_src = src_coord
    x_dst, y_dst, z_dst = dst_coord
    fraction = step / (num_steps - 1)

    x_step = x_src + fraction * (x_dst - x_src) if x_src is not None and x_dst is not None else x_src
    y_step = y_src + fraction * (y_dst - y_src) if y_src is not None and y_dst is not None else y_src
    z_step = z_src + fraction * (z_dst - z_src) if z_src is not None and z_dst is not None else z_src

    return x_step, y_step, z_step


def calculate_direction(normal):
    if normal[0] == 0 and normal[1] == 0:
        return np.array([1, 0, 0])
    else:
        return np.cross(normal, (0, 0, 1))
