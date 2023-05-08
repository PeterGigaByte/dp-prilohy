from src.user_settings import config

gui = config.get_gui_config()
parser = config.get_parser_config()


def window_size():
    return gui['width'] + 'x' + gui['height']


def window_title():
    return gui['title']


def open_button_label():
    return gui['open_button_label']


def show_info_label():
    return gui['show_info_label']


def appearance_mode():
    return gui['appearance_mode']


def color_theme():
    return gui['color_theme']


def icon():
    return gui['icon']


def select_file_image():
    return gui['select_file_image']


def start_simulation_image():
    return gui['start_simulation_image']


def start_simulation_label():
    return gui['start_simulation_label']


def resume_simulation_image():
    return gui['resume_simulation_image']


def resume_simulation_label():
    return gui['resume_simulation_label']


def pause_simulation_image():
    return gui['pause_simulation_image']


def pause_simulation_label():
    return gui['pause_simulation_label']


def resource_path():
    return gui['resource_path']


def canvas_bg_color():
    return gui['canvas_bg_color']


def canvas_width():
    return gui['canvas_width']


def canvas_height():
    return gui['canvas_height']


def frame_information_width():
    return gui['frame_information_width']


def frame_information_height():
    return gui['frame_information_height']


def frame_information_bg_color():
    return gui['frame_information_bg_color']


def bar_width():
    return gui['bar_width']


def text_color():
    return gui['text_color']


def node_img():
    return gui['node_img']


def xml_parser_type():
    return parser['xml']
