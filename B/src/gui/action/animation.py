import threading
from tkinter import filedialog as fd, W
from tkinter.messagebox import showinfo

import customtkinter
from PIL import ImageTk, Image

from src.data.objects.objects_definition import Node, P
from src.data.readers.json_reader import call_json_parser
from src.data.readers.xml_dom_reader import call_xml_dom_parser
from src.data.readers.xml_element_tree_reader import call_xml_tree_element_parser
from src.gui import window
from src.user_settings import settings
from src.utils.compute_utils import compute_coordinates_location, create_node_dict_with_coordinates
from src.utils.helper import get_file_extension
from src.utils.manager import get_objects_by_type


class Ns3VisualizerApp:
    def __init__(self):
        self.gui = window.Gui2D()
        self.menu = window.MenuFrame(self.gui)
        self.information_frame = window.InformationFrame(self.gui)
        self.simulation_canvas = window.SimulationCanvas(self.gui)

        # Data
        self.selected_data = ''
        self.type = ''
        self.actual_position = 0
        self.is_running_simulation = False
        self.nodes_text_info = ''
        self.multiplier = 10
        self.node_img = None
        self.nodes = []
        self.packet_simulation_objects = []
        self.node_dict = {}
        self.inf_text_id = ''
        self.line_id = ''
        self.line_id_to_delete = None
        self.inf_text_id_to_delete = None
        self.delay = int(self.menu.slider_button.get())
        self.is_next = False

        # Add handlers for buttons
        self.menu.open_button.configure(command=self.select_file)
        self.menu.start_button.configure(command=self.start_simulation)
        self.menu.resume_button.configure(command=self.resume_simulation)
        self.menu.pause_button.configure(command=self.pause_simulation)
        self.menu.slider_button.configure(command=self.change_delay)

        # Initialize scheduling
        self.initialize_scheduled_events()

    # Button Events
    # 1 selecting data event
    def select_file(self):
        filetypes = (
            ('Xml files', '*.xml'),
            ('Json files', '*.json'),
            ('All files', '*.')
        )

        filename = fd.askopenfilename(
            title=settings.open_button_label(),
            initialdir=settings.resource_path(),
            filetypes=filetypes)

        showinfo(
            title=settings.show_info_label(),
            message=filename
        )
        self.type = get_file_extension(filename)
        if self.type == 'xml':
            if settings.xml_parser_type() == 'treeElement':
                self.selected_data = call_xml_tree_element_parser(filename)
            elif settings.xml_parser_type() == 'dom':
                self.selected_data = call_xml_dom_parser(filename)
        elif self.type == 'json':
            self.selected_data = call_json_parser(filename)

    # 2 starting simulation event
    def start_simulation(self):
        self.node_img = ImageTk.PhotoImage(
            Image.open(settings.resource_path() + settings.node_img()).resize((50, 50), Image.ANTIALIAS))
        # 1. sets
        self.actual_position = 0
        self.is_running_simulation = True

        # 2. get nodes from data
        nodes = get_objects_by_type(self.selected_data[0].content, Node)
        nodes_size = 'Number of nodes in simulation: ' + str(len(nodes))

        # 3. show info about nodes
        self.nodes_text_info = customtkinter.CTkLabel(self.information_frame, text=nodes_size)
        self.nodes_text_info.grid(row=0, column=0, sticky=W, pady=2)

        # 4. show nodes
        for node in nodes:
            x, y = compute_coordinates_location(node.loc_x, node.loc_y, self.multiplier,
                                                int(settings.canvas_width()),
                                                int(settings.canvas_height()))

            # x = float(node.loc_x)
            # y = float(node.loc_y)
            node.loc_x = x
            node.loc_y = y
            self.nodes.append(self.simulation_canvas.create_image(x, y, anchor='nw', image=self.node_img))

        # 5. show packet simulation
        self.packet_simulation_objects = get_objects_by_type(self.selected_data[0].content, P)
        self.node_dict = create_node_dict_with_coordinates(nodes)

    # 3 Pause simulation
    def pause_simulation(self):
        self.is_running_simulation = False

    # 4 event to draw step of simulation
    def resume_simulation(self):
        self.clear_after_resume()
        self.is_running_simulation = True

    # 5 event to draw step of simulation
    def draw_lines(self):
        if self.is_running_simulation and len(
                self.packet_simulation_objects) > self.actual_position >= 0:
            if self.is_next:
                color = 'red'
                self.is_next = False
            else:
                color = 'blue'
                self.is_next = True
            from_id = self.packet_simulation_objects[self.actual_position].f_id
            to_id = self.packet_simulation_objects[self.actual_position].t_id
            information_text = 'From: ' + from_id + '   |  To: ' + to_id
            self.inf_text_id = customtkinter.CTkLabel(self.information_frame, text=information_text)
            self.inf_text_id.grid(row=0, column=2, sticky=W, pady=2)
            # to add spaced line dash=(5, 2)

            self.line_id = self.simulation_canvas.create_line(self.node_dict[from_id]['loc_x'] + 25,
                                                              self.node_dict[from_id]['loc_y'] + 25,
                                                              self.node_dict[to_id]['loc_x'] + 25,
                                                              self.node_dict[to_id]['loc_y'] + 25, fill=color,
                                                              arrow='last',
                                                              width=5)
            self.line_id_to_delete = self.simulation_canvas.after(self.delay, self.simulation_canvas.delete,
                                                                  self.line_id)
            pos = self.actual_position
            if pos != 0:
                pos = pos + 1
            percentage = pos / len(self.packet_simulation_objects)
            self.information_frame.progress_bar.set(percentage)
            self.information_frame.progress_bar_label.configure(text=str('{:.2f} %'.format(percentage * 100)))
            self.change_position()
            if self.actual_position == -1:
                self.simulation_canvas.after_cancel(self.line_id_to_delete)
                self.actual_position = 0
                self.is_running_simulation = False
                self.simulation_canvas.delete(self.line_id)
            if self.actual_position == len(self.packet_simulation_objects):
                self.actual_position = len(self.packet_simulation_objects) - 1
                self.is_running_simulation = False
                self.simulation_canvas.delete(self.line_id)

        self.simulation_canvas.after(self.delay, self.draw_lines)

    def initialize_scheduled_events(self):
        self.simulation_canvas.after(self.delay, self.draw_lines)
        self.stop_deleting()

    def stop_deleting(self):
        if not self.is_running_simulation and (self.line_id_to_delete or self.line_id_to_delete is not None):
            self.simulation_canvas.after_cancel(self.line_id_to_delete)
        threading.Timer(self.delay / 1000, self.stop_deleting).start()

    def clear_after_resume(self):
        if self.line_id is not None:
            self.simulation_canvas.delete(self.line_id)

    def change_delay(self, value):
        self.delay = int(value)

    def change_position(self):
        if self.menu.switch_button.get():
            self.actual_position = self.actual_position - 1
        else:
            self.actual_position = self.actual_position + 1
