from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from views.manage.dict import label_mapping


def create_input_fields(fields):
    widget = QWidget()
    layout = QVBoxLayout()

    inputs = {}

    for field in fields:
        layout.addWidget(QLabel(label_mapping[field] + ':'))
        inputs[field] = QLineEdit()
        layout.addWidget(inputs[field])

    widget.setLayout(layout)
    widget.inputs = inputs
    return widget
