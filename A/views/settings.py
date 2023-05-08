from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QDoubleSpinBox, QCheckBox


class SettingsView(QFrame):
    """
    A view for application settings.
    """

    def __init__(self, bottom_dock_widget, parent=None):
        """
        Initializes the view with a QVBoxLayout, labels, and spin boxes.
        """
        super(SettingsView, self).__init__(parent)

        self.parser_batch_size_callback = None
        self.processor_settings_callback = None
        self.animation_api_callback = None
        self.parser_change_callback = None
        self.bottom_dock_widget = bottom_dock_widget
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings view"))

        # Create the checkbox with a label
        self.use_optimized_parser = QCheckBox("Use database (Needs to be checked when using ElementTreeXmlParser)")

        # Add the checkbox to the layout
        layout.addWidget(self.use_optimized_parser)

        # Create the combo box
        self.select_field = QComboBox()
        self.select_field.addItem("ElementTreeXmlParser")
        self.select_field.addItem("DomXmlParser")

        # Add the combo box to the layout
        layout.addWidget(self.select_field)

        self.parser_batch_size_label = QLabel("Batch size for parser:")
        self.parser_batch_size_spinbox = QSpinBox()
        self.parser_batch_size_spinbox.setMinimum(1)
        self.parser_batch_size_spinbox.setMaximum(99999999)
        self.parser_batch_size_spinbox.setValue(150000)
        layout.addWidget(self.parser_batch_size_label)
        layout.addWidget(self.parser_batch_size_spinbox)

        self.processor_batch_size_label = QLabel("Batch size for processing:")
        self.processor_batch_size_spinbox = QSpinBox()
        self.processor_batch_size_spinbox.setMinimum(1)
        self.processor_batch_size_spinbox.setMaximum(99999999)
        self.processor_batch_size_spinbox.setValue(150000)
        layout.addWidget(self.processor_batch_size_label)
        layout.addWidget(self.processor_batch_size_spinbox)

        self.processor_database_batch_size_label = QLabel("Batch size for database processing:")
        self.processor_database_batch_size_spinbox = QSpinBox()
        self.processor_database_batch_size_spinbox.setMinimum(1)
        self.processor_database_batch_size_spinbox.setMaximum(99999999)
        self.processor_database_batch_size_spinbox.setValue(150000)
        layout.addWidget(self.processor_database_batch_size_label)
        layout.addWidget(self.processor_database_batch_size_spinbox)

        self.animation_batch_size_label = QLabel("Batch size for animation:")
        self.animation_batch_size_spinbox = QSpinBox()
        self.animation_batch_size_spinbox.setMinimum(1)
        self.animation_batch_size_spinbox.setMaximum(99999999)
        self.animation_batch_size_spinbox.setValue(150000)
        layout.addWidget(self.animation_batch_size_label)
        layout.addWidget(self.animation_batch_size_spinbox)

        self.wired_packet_label = QLabel("Steps per wired packet animation:")
        self.wired_packet_spinbox = QSpinBox()
        self.wired_packet_spinbox.setMinimum(2)
        self.wired_packet_spinbox.setMaximum(100)
        self.wired_packet_spinbox.setValue(20)
        layout.addWidget(self.wired_packet_label)
        layout.addWidget(self.wired_packet_spinbox)

        self.wireless_packet_label = QLabel("Steps per wireless packet animation:")
        self.wireless_packet_spinbox = QSpinBox()
        self.wireless_packet_spinbox.setMinimum(2)
        self.wireless_packet_spinbox.setMaximum(100)
        self.wireless_packet_spinbox.setValue(9)
        layout.addWidget(self.wireless_packet_label)
        layout.addWidget(self.wireless_packet_spinbox)

        self.num_steps_broadcast_transmission_label = QLabel("Steps per wireless transmission animation:")
        self.num_steps_broadcast_transmission_spinbox = QSpinBox()
        self.num_steps_broadcast_transmission_spinbox.setMinimum(2)
        self.num_steps_broadcast_transmission_spinbox.setMaximum(100)
        self.num_steps_broadcast_transmission_spinbox.setValue(12)
        layout.addWidget(self.num_steps_broadcast_transmission_label)
        layout.addWidget(self.num_steps_broadcast_transmission_spinbox)

        self.radius_constant_label = QLabel("Values for radius constant:")
        self.radius_constant_spinbox = QSpinBox()
        self.radius_constant_spinbox.setMinimum(2)
        self.radius_constant_spinbox.setMaximum(100)
        self.radius_constant_spinbox.setValue(2)
        layout.addWidget(self.radius_constant_label)
        layout.addWidget(self.radius_constant_spinbox)

        self.end_time_constant_label = QLabel("End time constant:")
        self.end_time_constant_spinbox = QDoubleSpinBox()
        self.end_time_constant_spinbox.setMinimum(0)
        self.end_time_constant_spinbox.setMaximum(100)
        self.end_time_constant_spinbox.setDecimals(6)
        self.end_time_constant_spinbox.setValue(0.000010)
        layout.addWidget(self.end_time_constant_label)
        layout.addWidget(self.end_time_constant_spinbox)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.processor_settings_callback(
            self.processor_batch_size_spinbox.value(), self.processor_database_batch_size_spinbox.value(), self.wired_packet_spinbox.value(),
            self.num_steps_broadcast_transmission_spinbox.value(), self.wireless_packet_spinbox.value(),
            self.radius_constant_spinbox.value(), self.end_time_constant_spinbox.value(), self.use_optimized_parser.isChecked()
        )
        self.animation_api_callback(
            self.wired_packet_spinbox.value(),
            self.wireless_packet_spinbox.value(),
            self.num_steps_broadcast_transmission_spinbox.value(),
            self.use_optimized_parser.isChecked(),
            self.animation_batch_size_spinbox.value()

        )
        self.parser_change_callback("xml", self.select_field.currentText())
        self.parser_batch_size_callback(self.parser_batch_size_spinbox.value())
        self.bottom_dock_widget.log("Settings were saved.")

    def set_processor_settings_callback(self, callback):
        self.processor_settings_callback = callback

    def set_animation_settings_callback(self, callback):
        self.animation_api_callback = callback

    def set_parser_change_callback(self, callback):
        self.parser_change_callback = callback

    def set_parser_batch_size_callback(self, callback):
        self.parser_batch_size_callback = callback
