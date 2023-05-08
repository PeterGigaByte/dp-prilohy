from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QProgressBar


class ControlHorizontal(QFrame):
    def __init__(self, vtk_api, animation_api, bottom_dock_widget, parent=None):
        super(ControlHorizontal, self).__init__(parent)
        self.vtk_api = vtk_api
        self.animation_api = animation_api
        self.bottom_dock_widget = bottom_dock_widget
        self.tasks = []

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignLeft)
        info_layout = QHBoxLayout()

        # Buttons
        # Play button
        self.play_button = QPushButton("Start")
        button_layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.on_play_button_clicked)

        # Pause button
        self.pause_button = QPushButton("Pause/Resume")
        button_layout.addWidget(self.pause_button)
        self.pause_button.clicked.connect(self.on_pause_button_clicked)

        # Reset button
        self.reset_button = QPushButton("Reset")
        button_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)

        # Create QVBoxLayout for progress bar and its label
        progress_layout = QVBoxLayout()

        # Add label above progress bar
        self.progress_bar_label = QLabel("Processing Progress:")
        progress_layout.addWidget(self.progress_bar_label)

        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        # Add progress layout to the button layout
        main_layout.addLayout(progress_layout)

        # Move ground_object up button
        self.move_ground_up_button = QPushButton("Move Ground Up")
        button_layout.addWidget(self.move_ground_up_button)
        self.move_ground_up_timer = QTimer(self)
        self.move_ground_up_timer.timeout.connect(self.on_move_ground_up_button_clicked)
        self.move_ground_up_button.pressed.connect(self.move_ground_up_timer.start)
        self.move_ground_up_button.released.connect(self.move_ground_up_timer.stop)

        # Move ground_object down button
        self.move_ground_down_button = QPushButton("Move Ground Down")
        button_layout.addWidget(self.move_ground_down_button)
        self.move_ground_down_timer = QTimer(self)
        self.move_ground_down_timer.timeout.connect(self.on_move_ground_down_button_clicked)
        self.move_ground_down_button.pressed.connect(self.move_ground_down_timer.start)
        self.move_ground_down_button.released.connect(self.move_ground_down_timer.stop)

        # Add information label about time
        self.left_info_label = QLabel()
        info_layout.addWidget(self.left_info_label)

        # Add additional label for time and align it to the right side
        self.right_info_label = QLabel()
        info_layout.addWidget(self.right_info_label, alignment=Qt.AlignRight)

        main_layout.addLayout(info_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def on_play_button_clicked(self):
        self.bottom_dock_widget.log("Play button pressed - Animation started.")
        self.animation_api.animate_substeps()

    def on_pause_button_clicked(self):
        if not self.animation_api.is_paused:
            self.bottom_dock_widget.log("Pause button pressed - Animation paused.")
            self.animation_api.pause_unpause_animation()
            self.pause_button.setText("Resume")
        else:
            self.bottom_dock_widget.log("Resume button pressed - Animation resumed.")
            self.animation_api.pause_unpause_animation()
            self.pause_button.setText("Pause")

    def on_reset_button_clicked(self):
        self.bottom_dock_widget.log("Reset button pressed - Animation reset.")
        self.animation_api.reset_animation()

    def update_status(self, left_info_label_text, right_info_label_text, actual_value, maximum, label_text):
        """Update left and right text of the information label."""
        self.left_info_label.setText(left_info_label_text)
        self.right_info_label.setText(right_info_label_text)
        self.update_progress_bar(actual_value, maximum, label_text)

    def on_move_ground_up_button_clicked(self):
        self.bottom_dock_widget.log("Move Ground Up button pressed - Ground moved up.")
        self.animation_api.renderer_api.ground.move_ground(1,
                                                           self.animation_api.renderer_api.renderer)  # step size for moving the ground_object up

    def on_move_ground_down_button_clicked(self):
        self.bottom_dock_widget.log("Move Ground Down button pressed - Ground moved down.")
        self.animation_api.renderer_api.ground.move_ground(-1,
                                                           self.animation_api.renderer_api.renderer)  # step size for moving the ground_object down

    def show_progress_bar(self):
        """Show the progress bar."""
        self.progress_bar.show()  # Show the progress bar

    def update_progress_bar(self, actual_value, maximum, label_text):
        """Update the value of the progress bar."""
        self.progress_bar.setValue(actual_value)  # Update the value of the progress bar
        self.progress_bar.setMaximum(maximum)  # Update the maximum value of the progress bar
        self.progress_bar_label.setText(label_text)
