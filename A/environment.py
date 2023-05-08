import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QMenu, QFrame, QFileDialog, QStackedWidget, QGridLayout
)

from api.animation import AnimationApi

from api.rendering.rendering import EnvironmentRenderingApi
from components.dock_widgets.bottom_dock_widget import BottomDockWidget
from components.dock_widgets.left_dock_widget import LeftDockWidget
from components.dock_widgets.right_dock_widget import RightDockWidget
from components.frames.bottom import BottomFrame
from components.frames.control_horizontal import ControlHorizontal
from components.frames.control_vertical import ControlVertical
from components.tutorialPopUp import show_tutorial
from convertors.json_convertor import xml_convert_to_json
from database.database import get_steps, get_all_nodes, get_all_nonp2plinkproperties, save_to_database
from interactors.interactors import CustomInteractorStyle, KeyPressInteractor
from network_elements.elements import Node, NonP2pLinkProperties
from parsers.json.json_parser import JsonParser
from parsers.parser import ParserAPI
from parsers.xml.dom import DomXmlParser
from parsers.xml.tree_element import ElementTreeXmlParser
from step.step_processor import StepProcessor
from utils.manage import get_objects_by_type
from views.manage.manage import ManageCustomView
from views.settings import SettingsView

"""A class that represents an environment visualization.

This class is a PyQt5-based GUI that allows users to open and visualize files containing data about nodes and buildings.
The GUI includes a menu bar with options to open files, switch between different views, and access help.
The visualization itself is created using the VTK library and allows users to control the animation and view settings.

Attributes:
    bottom_dock_widget (BottomDockWidget): A widget that displays status updates and logs.
    interactor (KeyPressInteractor): A custom interactor for handling keyboard inputs.
    visualizing_frame (QFrame): A frame for displaying the VTK visualization.
    left_dock_widget (LeftDockWidget): A widget for displaying information about nodes.
    right_dock_widget (RightDockWidget): A widget for displaying information about buildings.
    parser_api (ParserAPI): An API for parsing files containing data about nodes and buildings.
    vtk_api (EnvironmentRenderingApi): An API for rendering the environment using VTK.
    step_processor (StepProcessor): A processor for breaking down animation steps into substeps.
    animation_api (AnimationApi): An API for controlling the animation.
    stacked_widget (QStackedWidget): A widget for switching between different views.

Methods:
    create_menu(): Creates the menu bar for the application.
    visualizing_view(): Switches to the visualizing view.
    settings_view(): Switches to the settings view.
    manage_custom_view(): Switches to the manage custom objects view.
    create_visualizing_view(): Creates the visualizing view.
    showEvent(event): Handles show events for the QMainWindow.
    open_file(): Opens a file and processes its contents.
"""


class Environment(QMainWindow):
    def __init__(self, parent=None):
        super(Environment, self).__init__(parent)

        self.file_path = None
        self.control_horizontal = None
        self.control_vertical = None
        self.bottom_dock_widget = None
        self.interactor = None
        self.visualizing_frame = None
        self.left_dock_widget = LeftDockWidget(self)
        self.right_dock_widget = RightDockWidget(self)
        self.bottom_dock_widget = BottomDockWidget(self)
        self.setWindowTitle("Environment Visualization")
        self.resize(1000, 800)
        icon_path = os.path.join(os.getcwd(), "icons", "window_icon.png")
        self.setWindowIcon(QIcon(icon_path))

        # Initialize ParserAPI and register parsers
        self.parser_api = ParserAPI()
        element_tree_parser = ElementTreeXmlParser(bottom_dock_widget=self.bottom_dock_widget)
        dom_parser = DomXmlParser(bottom_dock_widget=self.bottom_dock_widget)
        dom_parser.parsed_data_signal.connect(self.set_parsed_data)

        json_parser = JsonParser(bottom_dock_widget=self.bottom_dock_widget)
        json_parser.parsed_data_signal.connect(self.set_parsed_data)

        self.parser_api.register_parser('xml', element_tree_parser,
                                        "ElementTreeXmlParser")
        self.parser_api.register_parser('xml', dom_parser, "DomXmlParser")
        self.parser_api.register_parser('json', json_parser, "JsonParser")

        # Initialize EnvironmentRenderingApi
        self.vtk_api = EnvironmentRenderingApi()
        self.renderer = self.vtk_api.get_renderer()

        # Initialize StepProcessor
        self.step_processor = StepProcessor(self.bottom_dock_widget)

        # Initialize AnimationAPI
        self.animation_api = AnimationApi(self.vtk_api, self.bottom_dock_widget)

        self.interactor_style = CustomInteractorStyle()

        # Initialize StackedWidget
        self.stacked_widget = QStackedWidget()

        # Create menu and render window
        self.create_menu()

        # Initialize views
        self.visualizing_view_widget = self.create_visualizing_view()
        self.settings_view_widget = SettingsView(self.bottom_dock_widget)
        self.settings_view_widget.set_processor_settings_callback(self.step_processor.update_constants)
        self.settings_view_widget.set_animation_settings_callback(self.animation_api.update_steps_constants)
        self.settings_view_widget.set_parser_change_callback(self.parser_api.set_active_parser)
        self.settings_view_widget.set_parser_batch_size_callback(self.parser_api.set_batch_size)
        self.manage_custom_view_widget = ManageCustomView(self)

        # Add views to the stacked widget
        self.stacked_widget.addWidget(self.visualizing_view_widget)
        self.stacked_widget.addWidget(self.settings_view_widget)
        self.stacked_widget.addWidget(self.manage_custom_view_widget)

        # Set the initial view
        self.stacked_widget.setCurrentWidget(self.visualizing_view_widget)

        # Set the central widget to the stacked widget
        self.setCentralWidget(self.stacked_widget)

    def create_menu(self):
        """Create the menu bar for the application."""

        # Open file menu
        open_file = QMenu("File", self)
        open_file.addAction("Open File", self.open_file)

        # Convert xml to json file menu
        open_file.addAction("Convert xml to json", self.convert_to_json)

        # View menu
        view_menu = QMenu("View", self)
        view_menu.addAction("Visualizing", self.visualizing_view)
        view_menu.addAction("Settings", self.settings_view)
        view_menu.addAction("Manage custom", self.manage_custom_view)

        # View menu
        run_menu = QMenu("Run", self)
        run_menu.addAction("Parse file", self.parse_file)
        run_menu.addAction("Process data", self.process_data)
        run_menu.addAction("Start animation", self.run_animation)
        run_menu.addAction("Parse && Process && Start animation ", self.parse_process_run)

        # Help menu
        help_menu = QMenu("Help", self)
        help_menu.addAction("Tutorial", show_tutorial)

        # Menu bar
        menu_bar = self.menuBar()
        menu_bar.addMenu(open_file)
        menu_bar.addMenu(view_menu)
        menu_bar.addMenu(run_menu)
        menu_bar.addMenu(help_menu)

    def visualizing_view(self):
        """Switch to the visualizing view."""
        self.stacked_widget.setCurrentWidget(self.visualizing_view_widget)

    def settings_view(self):
        """Switch to the settings view."""
        self.stacked_widget.setCurrentWidget(self.settings_view_widget)

    def manage_custom_view(self):
        """Switch to the manage custom objects view."""
        self.stacked_widget.setCurrentWidget(self.manage_custom_view_widget)

    def create_visualizing_view(self):
        visualizing_view = QFrame(self)
        self.setCentralWidget(visualizing_view)

        # interactor
        self.interactor = KeyPressInteractor(visualizing_view)
        self.interactor.Initialize()

        self.interactor.setFocusPolicy(Qt.StrongFocus)
        self.interactor.setFocus()

        layout = QGridLayout()

        # Create the ControlVertical instance
        self.control_vertical = ControlVertical(self.animation_api)

        # Top control frame init (ControlHorizontal)
        self.control_horizontal = ControlHorizontal(vtk_api=self.vtk_api, animation_api=self.animation_api,
                                                    bottom_dock_widget=self.bottom_dock_widget)
        self.animation_api.set_control_update_callback(self.control_horizontal.update_status)
        self.animation_api.set_max_steps_callback(self.control_vertical.update_max_step_slider)
        self.animation_api.set_update_steps_callback(self.control_vertical.update_value_steps)

        # Left dock Widget frame init
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock_widget)

        # Right dock Widget frame init
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock_widget)

        # Bottom dock Widget frame init
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock_widget)

        # Bottom Time frame init
        bottom_frame = BottomFrame(self)

        # Adding widgets
        layout.addWidget(self.control_horizontal, 0, 0, 1, 2)  # ControlHorizontal spans 2 columns
        layout.addWidget(self.interactor, 1, 0)  # VTK window
        layout.addWidget(self.control_vertical, 1, 1)  # ControlVertical
        layout.addWidget(bottom_frame, 2, 0, 1, 2)  # BottomFrame spans 2 columns

        visualizing_view.setLayout(layout)

        render_window = self.interactor.GetRenderWindow()
        render_window.AddRenderer(self.renderer)
        render_window.SetSize(1000, 800)
        render_window.SetWindowName("Environment Visualization")

        self.vtk_api.test_view()  # Test view // remove

        self.interactor_style.SetCurrentRenderer(self.renderer)
        self.interactor.SetInteractorStyle(self.interactor_style)
        return visualizing_view

    def showEvent(self, event):
        """Handle show events for the QMainWindow."""
        super().showEvent(event)
        self.interactor.setFocus()

    def open_file(self):
        """Open a file and process its contents."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Xml Files (*.xml);;Json "
                                                                               "Files (*.json)",
                                                        options=options)
        self.bottom_dock_widget.log(f"File opened: {self.file_path}")
        # reset everything - to avoid issues when opening second file
        self.reset_when_file_open()

    def convert_to_json(self):

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Xml Files (*.xml)",
                                                   options=options)
        if file_path:
            xml_convert_to_json(file_path)

    def reset_when_file_open(self):
        save_to_database([])
        self.animation_api.substeps = []
        self.step_processor.substeps = self.step_processor.substeps = {step_type: [] for step_type in
                                                                       self.step_processor.step_types}
        self.animation_api.data = None
        self.animation_api.reset_animation()
        self.control_horizontal.pause_button.setText("Pause/Resume")

    def process_data(self):
        if self.step_processor.optimized_parser:
            self.step_processor.data = None
            self.step_processor.data_processed.connect(self.on_data_processed)
            self.step_processor.update_status.connect(self.on_status_update)
            self.step_processor.start()
        elif self.file_path and self.animation_api.data is not None:
            self.step_processor.data = self.animation_api.data
            self.step_processor.data_processed.connect(self.on_data_processed)
            self.step_processor.start()

            self.left_dock_widget.clear_widgets()
            self.left_dock_widget.update_list_widget(get_objects_by_type(self.animation_api.data.content, Node), get_objects_by_type(self.animation_api.data.content, NonP2pLinkProperties))
            self.animation_api.prepare_animation()
            self.visualizing_view()
        else:
            self.bottom_dock_widget.log("File path is wrong.")

    def on_data_processed(self, result):
        if self.step_processor.optimized_parser:
            self.animation_api.set_substeps(get_steps(self.settings_view_widget.parser_batch_size_spinbox.value(), 0))
            self.left_dock_widget.clear_widgets()
            self.left_dock_widget.update_list_widget(get_all_nodes(), get_all_nonp2plinkproperties())
        else:
            self.animation_api.set_substeps(result)

    def on_status_update(self, current_index, maximum, time, text_label):
        self.control_horizontal.update_status(
            f"Step {current_index} / {maximum}",
            f"Time {str(round(time, 2))}",
            current_index,
            maximum,
            text_label)

    def parse_file(self):
        if self.file_path:
            self.reset_when_file_open()
            self.left_dock_widget.clear_widgets()
            self.animation_api.set_data(self.parser_api.parse_file(self.file_path))
        else:
            self.bottom_dock_widget.log("File path is wrong.")

    def set_parsed_data(self, result):
        self.animation_api.set_data(result)

    def run_animation(self):
        if self.settings_view_widget.use_optimized_parser.isChecked():
            self.animation_api.clear_vtk_window()
            self.animation_api.set_substeps(get_steps(self.settings_view_widget.parser_batch_size_spinbox.value(), 0))
            self.left_dock_widget.clear_widgets()
            self.left_dock_widget.update_list_widget(get_all_nodes(), get_all_nonp2plinkproperties())
            self.animation_api.prepare_animation()
            self.animation_api.animate_substeps()
        elif self.animation_api.data is not None:
            self.bottom_dock_widget.log("Run pressed - Animation started.")
            self.animation_api.animate_substeps()
        else:
            self.bottom_dock_widget.log("No data to animate.")

    def parse_process_run(self):
        self.parse_file()
        self.process_data()
        self.run_animation()
