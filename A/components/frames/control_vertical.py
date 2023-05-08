from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QSpinBox

from components.frames.custom.custom_slider import CustomSlider
from components.frames.custom.custom_spin_box import CustomSpinBox


class ControlVertical(QFrame):
    def __init__(self, animation_api, parent=None):
        super(ControlVertical, self).__init__(parent)
        self.initial_slider_value = None
        self.animation_api = animation_api

        layout = QHBoxLayout()

        # Delay slider
        delay_layout = QVBoxLayout()
        delay_layout.addWidget(QLabel("\nDelay\n(ms):"))
        self.delay_slider = QSlider(Qt.Vertical)
        self.delay_slider.setMinimum(0)
        self.delay_slider.setMaximum(1000)
        self.delay_slider.setValue(self.animation_api.delay)
        self.delay_slider.valueChanged.connect(self.on_delay_slider_changed)
        delay_layout.addWidget(self.delay_slider)
        self.delay_value_label = QSpinBox()
        self.delay_value_label.setValue(self.animation_api.delay)
        self.delay_value_label.setRange(0, 1000)
        self.delay_value_label.editingFinished.connect(self.on_delay_value_label_changed)
        delay_layout.addWidget(self.delay_value_label)
        layout.addLayout(delay_layout)

        # Steps per event slider
        steps_layout = QVBoxLayout()
        steps_layout.addWidget(QLabel("Steps\nper\nevent:"))
        self.steps_per_event_slider = QSlider(Qt.Vertical)
        self.steps_per_event_slider.setMinimum(1)
        self.steps_per_event_slider.setMaximum(100)
        self.steps_per_event_slider.setValue(1)
        self.steps_per_event_slider.valueChanged.connect(self.on_steps_per_event_slider_changed)
        steps_layout.addWidget(self.steps_per_event_slider)
        self.steps_per_event_value_label = CustomSpinBox()
        self.steps_per_event_value_label.setValue(1)
        self.steps_per_event_value_label.setRange(1, 100)
        self.steps_per_event_value_label.editingFinished.connect(self.on_steps_per_event_label_changed)

        steps_layout.addWidget(self.steps_per_event_value_label)
        layout.addLayout(steps_layout)

        # Step slider
        step_layout = QVBoxLayout()
        step_layout.addWidget(QLabel("\n\nStep:"))
        self.step_slider = CustomSlider(Qt.Vertical)
        self.step_slider.setMinimum(0)
        self.step_slider.setMaximum(100)
        self.step_slider.setValue(0)
        self.step_slider.setTickInterval(1)
        self.step_slider.sliderReleased.connect(self.on_step_slider_released)
        self.step_slider.sliderPressed.connect(self.on_step_slider_pressed)
        step_layout.addWidget(self.step_slider)
        self.step_value_label = CustomSpinBox()
        self.step_value_label.setValue(0)
        self.step_value_label.setRange(0, 100)
        self.step_value_label.editingStarted.connect(self.animation_api.pause_animation)
        self.step_value_label.editingFinished.connect(self.on_steps_value_label_changed)
        self.delay_value_label.valueChanged.connect(self.on_delay_value_label_changed)
        step_layout.addWidget(self.step_value_label)
        layout.addLayout(step_layout)

        self.setLayout(layout)

    # Add slider logic methods here
    def on_delay_slider_changed(self, value):
        self.animation_api.update_delay(value)
        self.delay_value_label.setValue(value)

    def on_steps_per_event_slider_changed(self, value):
        self.animation_api.steps_per_event = value
        self.steps_per_event_value_label.setValue(value)

    def on_step_slider_changed(self, value):
        self.animation_api.set_current_step(value)
        self.step_value_label.setValue(value)

    def on_step_slider_pressed(self):
        self.animation_api.was_paused = self.animation_api.is_paused
        self.animation_api.pause_animation()
        self.initial_slider_value = self.step_slider.value()

    def on_step_slider_released(self):
        new_slider_value = self.step_slider.value()
        if new_slider_value != self.initial_slider_value:
            self.on_step_slider_changed(new_slider_value)
        if not self.animation_api.was_paused:
            self.animation_api.unpause_animation()

    def update_max_step_slider(self, maximum_steps):
        self.step_slider.setMaximum(maximum_steps)
        self.step_value_label.setRange(0, maximum_steps)

    # Add this new method in the ControlVertical class
    def update_value_steps(self, value):
        self.step_slider.setValue(value)
        self.step_value_label.setValue(value)

    def on_delay_value_label_changed(self):
        value = self.delay_value_label.value()
        self.delay_slider.setValue(value)
        self.animation_api.update_delay(value)

    def on_steps_value_label_changed(self):
        value = self.step_value_label.value()
        self.step_slider.setValue(value)
        self.animation_api.set_current_step(value)
        if not self.animation_api.was_paused:
            self.animation_api.unpause_animation()

    def on_steps_per_event_label_changed(self):
        self.animation_api.steps_per_event = self.steps_per_event_value_label.value()
        self.steps_per_event_slider.setValue(self.steps_per_event_value_label.value())
