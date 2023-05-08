from views.manage.object_creation import create_node, create_building, create_arrow

# Define strings
object_str = 'Object'
relation_str = 'Relation'
node_str = 'Node'
building_str = 'Building'
line_with_arrow_str = 'Line with arrow'
line_without_arrow_str = 'Line without arrow'

input_field_configs = {
    node_str: ['x', 'y', 'z'],
    building_str: ['x', 'y', 'z', 'width', 'height'],
    line_with_arrow_str: ['x1', 'y1', 'z1', 'x2', 'y2', 'z2'],
    line_without_arrow_str: ['x1', 'y1', 'z1', 'x2', 'y2', 'z2'],
}

object_subtype_configs = {
    object_str: [node_str, building_str],
    relation_str: [line_with_arrow_str, line_without_arrow_str],
}

object_creation_functions = {
    object_str: {
        node_str: create_node,
        building_str: create_building,
    },
    relation_str: {
        line_with_arrow_str: create_arrow,  # replace with the corresponding function
        line_without_arrow_str: None,  # replace with the corresponding function
    },
}

label_mapping = {
    'x': 'X coor',
    'y': 'Y coor',
    'z': 'Z coor',
    'width': 'Width',
    'height': 'Height',
    'x1': 'X1 coor',
    'y1': 'Y1 coor',
    'z1': 'Z1 coor',
    'x2': 'X2 coor',
    'y2': 'Y2 coor',
    'z2': 'Z2 coor',
}
