from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QListWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QWidget

from utils.manage import get_nonp2p_link_properties_by_node_id


class LeftDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(LeftDockWidget, self).__init__("Nodes", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)

        # Create the list widget and add it to the layout
        self.list_widget = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        # Create the tree widget and add it to the layout
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        layout.addWidget(self.tree_widget)

        # Initialize empty node_object dictionary
        self.nodes = {}

        # Connect to the list widget's item selection changed signal_object and update the tree widget's content accordingly
        self.list_widget.itemSelectionChanged.connect(self.update_tree_widget)

        # Create a widget to hold the layout and set it as the dock widget's widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)

    def add_node(self, node_id, properties=None):
        if properties is None:
            properties = []

        self.list_widget.addItem(f"Node {node_id}")
        self.nodes[node_id] = {"properties": properties}

    def add_node_property(self, node_id, parent_item, property_name, fourth_level_values=None):
        groups = ["IP", "MAC"]
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist")

        if fourth_level_values is None:
            fourth_level_values = []

        second_level_item = QTreeWidgetItem(parent_item, [property_name])
        for i, group_name in enumerate(groups):
            third_level_item = QTreeWidgetItem(second_level_item, [group_name])
            if i < len(fourth_level_values):
                for fourth_level_value in fourth_level_values[i]:
                    QTreeWidgetItem(third_level_item, [str(fourth_level_value)])

    def update_node_property(self, node_id, property_name, values):
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist")

        for prop in self.nodes[node_id]["properties"]:
            if prop.text(0) == property_name:
                for i, value in enumerate(values):
                    prop.child(i).setText(0, value)

    def update_tree_widget(self):
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) > 0:
            selected_item = selected_items[0].text()
            node_id = selected_item.split(" ")[1]

            # Clear tree widget and display selected node_object properties
            self.tree_widget.clear()
            for prop in self.nodes[int(node_id)]["properties"]:
                # Clone the QTreeWidgetItem before adding it to the tree widget
                cloned_prop = prop.clone()
                self.tree_widget.addTopLevelItem(cloned_prop)

    def update_list_widget(self, nodes, nonp2p_link_properties_list):
        for node in nodes:
            channel_type_list, channel_type_dict = get_nonp2p_link_properties_by_node_id(nonp2p_link_properties_list,
                                                                                         node.id)
            self.add_node(node.id)

            channel_type_root = QTreeWidgetItem(None, ["Channel type"])
            self.nodes[node.id]["properties"].append(channel_type_root)

            for channel_type in channel_type_list:
                ip_list = channel_type_dict[channel_type]['ips']
                mac_list = channel_type_dict[channel_type]['macs']
                self.add_node_property(node.id, channel_type_root, channel_type, [ip_list, mac_list])

    def clear_widgets(self):
        self.list_widget.clear()
        self.tree_widget.clear()
