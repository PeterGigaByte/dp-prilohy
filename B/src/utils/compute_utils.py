def compute_coordinates_location(x, y, multiplier, screen_width, screen_height):
    x = float(x) * multiplier
    y = float(y) * multiplier

    while x > screen_width or x < 0:
        if x > screen_width:
            x = x - screen_width
        else:
            x = x + screen_width
    while y > screen_height or y < 0:
        if y > screen_height:
            y = y - screen_height
        else:
            y = y + screen_height

    return x, y


def create_node_dict_with_coordinates(nodes):
    nodes_dict = {}
    for node in nodes:
        nodes_dict[node.id] = {'loc_x': node.loc_x, 'loc_y': node.loc_y}
    return nodes_dict
