from PyQt5.QtWidgets import QPushButton, QStackedWidget, QComboBox, QVBoxLayout, QFrame, QLabel

from views.manage.dict import object_creation_functions, object_subtype_configs, input_field_configs
from views.manage.input_fields import create_input_fields


def get_stacked_widget_index(category, subtype):
    if not subtype:
        return -1

    index_offset = 0
    for prev_category, subtypes in object_subtype_configs.items():
        if prev_category == category:
            return index_offset + subtypes.index(subtype)
        index_offset += len(subtypes)

    return -1


class ManageCustomView(QFrame):
    def __init__(self, environment, parent=None):
        super(ManageCustomView, self).__init__(parent)
        self.environment = environment

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Manage custom objects view"))

        # Add a QComboBox (select input) for selecting a category
        self.category_select_input = QComboBox()
        for category in object_subtype_configs.keys():
            self.category_select_input.addItem(category)
        layout.addWidget(self.category_select_input)

        # Add a QComboBox (select input) for selecting an object subtype
        self.subtype_select_input = QComboBox()
        layout.addWidget(self.subtype_select_input)

        # Create a StackedWidget to hold different sets of input fields
        self.stacked_inputs = QStackedWidget()

        # Add input fields to the StackedWidget
        for category, input_fields in input_field_configs.items():
            input_widget = create_input_fields(input_fields)
            self.stacked_inputs.addWidget(input_widget)

        layout.addWidget(self.stacked_inputs)

        # Add a QPushButton with the text "Submit"
        self.submit_button = QPushButton("Submit")
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Connect signals
        self.category_select_input.currentIndexChanged.connect(self.update_subtype_select_input)
        self.subtype_select_input.currentIndexChanged.connect(self.update_input_fields)
        self.submit_button.clicked.connect(self.submit_button_clicked)

        # Initialize subtype select input with the initial category
        self.update_subtype_select_input()

    def update_subtype_select_input(self):
        category = self.category_select_input.currentText()
        subtypes = object_subtype_configs[category]

        self.subtype_select_input.clear()
        for subtype in subtypes:
            self.subtype_select_input.addItem(subtype)

        self.update_input_fields()

    def update_input_fields(self):
        category = self.category_select_input.currentText()
        subtype = self.subtype_select_input.currentText()
        index = get_stacked_widget_index(category, subtype)
        self.stacked_inputs.setCurrentIndex(index)

    def submit_button_clicked(self):
        current_inputs = self.stacked_inputs.currentWidget().inputs
        category = self.category_select_input.currentText()
        subtype = self.subtype_select_input.currentText()
        create_function = object_creation_functions[category][subtype]
        create_function(self.environment, current_inputs)
