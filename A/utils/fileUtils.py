import json

import xmltodict


def xml_convert_to_json(path):
    with open(path) as xml_file:
        json_data = json.dumps(xmltodict.parse(xml_file.read()))
        with open(get_file_name(path) + '.json', "w") as json_file:
            json_file.write(json_data)


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1]


def get_file_name(filename):
    return filename.rsplit('.', 1)[0]
