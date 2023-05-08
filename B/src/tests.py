import logging

from gui.action.animation import Ns3VisualizerApp
from src.data.convetor.json_convertor import xml_convert_to_json
from src.data.objects.objects_definition import Node, Nu, Ip, Ncs, Wpr, Pr, Link, IpV6, Res, P, Address, \
    NonP2pLinkProperties
from src.data.readers.json_reader import call_json_parser
from src.data.readers.xml_dom_reader import call_xml_dom_parser
from src.data.readers.xml_element_tree_reader import call_xml_tree_element_parser
from utils.manager import get_objects_by_type

# Allowed tests in current state
allowed_tests_config = {
    'initialize_window_test': True,
    'none_type_test': True,
    'retrieve_objects_test': True,
    'parsing_test': True,
    'show_nodes_test': True,
    'simulate_communication_test': True,
    'arc_test': True
}

resources_path = '../resources/'

# List of possible objects
object_test_types = [Node, Nu, NonP2pLinkProperties, Ip, Address, Ncs, P, Wpr, Pr, Res, Link, IpV6]


# Code that is testing if count of unknown tags are zero
def none_type_test(none_type, filename):
    if allowed_tests_config['none_type_test'] is False:
        return
    assert none_type == 0, 'Parsing test failed for file ' + filename + ' - none type should be zero!'


# Testing parsing of file from resources
def parsing_test(filename, json_filename):
    if allowed_tests_config['parsing_test'] is False:
        return
    parsed_xml_tree_element, none_type = call_xml_tree_element_parser(filename)
    parsed_xml_dom = call_xml_dom_parser(filename)
    parsed_json = call_json_parser(json_filename)
    # ISSUE NonP2pLinkProperties
    assert len(parsed_xml_dom.content) == len(parsed_xml_tree_element.content)
    assert len(parsed_json.content) == len(parsed_xml_tree_element.content)
    # Tests
    none_type_test(none_type, filename)

    retrieve_objects_test(parsed_xml_tree_element.content, filename)
    return parsed_xml_tree_element


# Testing displaying window
def initialize_window_test():
    if allowed_tests_config['initialize_window_test'] is False:
        return
    Ns3VisualizerApp().gui.mainloop()


# Testing functionality to get objects from parsing
def retrieve_objects_test(objects, filename):
    if allowed_tests_config['retrieve_objects_test'] is False:
        return
    for object_type in object_test_types:
        objects_result = get_objects_by_type(objects, object_type)
        for item in objects_result:
            assert isinstance(item, object_type), 'Retrieve objects test failed for file ' + filename + \
                                                  ' - ' + type(item) + ' not equals ' + type(object_type)


def json_conversion_test(path):
    xml_convert_to_json(path)


# Initialization function of tests
if __name__ == '__main__':
    logging.basicConfig(filename='../tests.log', encoding='utf-8', level=logging.DEBUG)

    first_test_file_path_xml = resources_path + 'jj.xml'
    second_test_file_path_xml = resources_path + 'cc.xml'
    third_test_file_path_xml = resources_path + 'ns3.xml'

    first_test_file_path_json = resources_path + 'jj.json'
    second_test_file_path_json = resources_path + 'cc.json'
    third_test_file_path_json = resources_path + 'ns3.json'

    # Parsing tests
    first_xml_test_data = parsing_test(first_test_file_path_xml, first_test_file_path_json)
    second_xml_test_data = parsing_test(second_test_file_path_xml, second_test_file_path_json)
    third_xml_test_data = parsing_test(third_test_file_path_xml, third_test_file_path_json)

    # Conversion tests
    first_json_test_data = xml_convert_to_json(first_test_file_path_xml)
    second_json_test_data = xml_convert_to_json(second_test_file_path_xml)
    third_json_test_data = xml_convert_to_json(third_test_file_path_xml)

    # Json Parsing tests
    call_json_parser(first_test_file_path_json)
    call_json_parser(second_test_file_path_json)
    call_json_parser(third_test_file_path_json)

    # Window should be displayed
    initialize_window_test()
