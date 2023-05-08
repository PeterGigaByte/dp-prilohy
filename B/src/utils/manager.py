def get_objects_by_type(objects, object_type):
    return [item for item in objects if isinstance(item, object_type)]
