import json
import logging

import xmltodict

from utils.fileUtils import get_file_name


def xml_convert_to_json(path):
    logging.debug('Xml conversion to json')
    logging.debug('File path: {0}'.format(path))
    with open(path) as xml_file:
        json_data = json.dumps(xmltodict.parse(xml_file.read()))
        with open(get_file_name(path) + '.json', "w") as json_file:
            json_file.write(json_data)
