import uuid
from typing import Dict

import vtk

from api.rendering.rendering_objects.building_object.building import Building
from api.rendering.rendering_objects.donut_object.donut import Donut
from api.rendering.rendering_objects.ground_object.ground import Ground
from api.rendering.rendering_objects.node_object.node import Node
from api.rendering.rendering_objects.packet_object.packet import Packet
from api.rendering.rendering_objects.signal_object.broadcaster_signal import BroadcasterSignal
from api.rendering.rendering_objects.signal_object.wifi_signal import WifiSignal


def normalize_rgb(rgb):
    return tuple(channel / 255.0 for channel in rgb)


class EnvironmentRenderingApi:
    def __init__(self):
        self.renderer = vtk.vtkRenderer()
        self.setup_renderer()
        self.ground = None
        self.nodes = []
        self.buildings = []
        self.packets = []
        self.signals = {}
        self.packets: Dict[uuid.UUID, Packet] = {}
        self.wireless_packets: Dict[uuid.UUID, Donut] = {}

    def create_ground(self):
        """Create a ground_object plane for the environment."""
        self.ground = Ground(resolution=(200, 200), origin=(-500, -500, 0), point1=(500, -500, 0),
                             point2=(-500, 500, 0),
                             color=(0, 1, 0))
        self.ground.add_to_renderer(self.renderer)

    def create_building(self, x, y, z, width, height):
        """Create a building_object at the specified location."""
        building = Building(x=x, y=y, z=z, width=width, height=height)
        building.add_to_renderer(self.renderer)
        self.buildings.append(building)

    def create_node(self, id, x, y, z, radius=1, description="Node", node_color=(255, 0, 0),
                    label_color=(255, 255, 255)):
        """Create a node_object at the specified location."""
        node = Node(x=float(x), y=float(y), z=float(z), radius=radius, description=description, node_color=node_color,
                    label_color=label_color, node_id=id)
        node.add_to_renderer(renderer=self.renderer)
        self.nodes.append(node)

    def clear_vtk_window(self):
        # Remove all actors from the renderer
        for node in self.nodes:
            sphere_actor, text_actor = node
            self.renderer.RemoveActor(sphere_actor)
            self.renderer.RemoveActor(text_actor)

        # Clear the list of nodes
        self.nodes = []

        # Update the render window
        self.renderer.GetRenderWindow().Render()

    def create_packet(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        """Create a packet_object at the specified location."""
        packet_id = packet_id if packet_id else uuid.uuid4()
        packet = Packet(x, y, z, size=size, color=color, packet_id=packet_id)
        packet.add_to_renderer(self.renderer)

        # Store the packet_object object in the dictionary
        self.packets[packet_id] = packet

    def create_wireless_packet(self, x, y, z, size=1, color=(0, 0, 255), packet_id=None):
        """Create a packet_object at the specified location."""
        packet_id = packet_id if packet_id else uuid.uuid4()
        packet = Donut(x, y, z, size=size, color=color, packet_id=packet_id)
        packet.add_to_renderer(self.renderer)

        # Store the packet_object object in the dictionary
        self.wireless_packets[packet_id] = packet

    def remove_packet(self, packet_id):
        """Remove the specified packet_object from the environment."""
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.remove_from_renderer(self.renderer)
            del self.packets[packet_id]

    def remove_wireless_packet(self, packet_id):
        """Remove the specified packet_object from the environment."""
        if packet_id in self.wireless_packets:
            packet = self.wireless_packets[packet_id]
            packet.remove_from_renderer(self.renderer)
            del self.wireless_packets[packet_id]

    def update_packet_position(self, packet_id, x, y, z):
        """Update the position of the specified packet_object."""
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.update_position(x, y, z)

    def update_wireless_packet_position(self, packet_id, x, y, z):
        """Update the position of the specified packet_object."""
        if packet_id in self.wireless_packets:
            packet = self.wireless_packets[packet_id]
            packet.update_position(x, y, z)
            self.renderer.GetRenderWindow().Render()

    def setup_renderer(self):
        """Set up the renderer for the visualization."""
        self.renderer.SetBackground(0.5, 0.5, 0.5)
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(0, -500, 200)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 0, 1)
        camera.SetClippingRange(1, 1000)

    def get_renderer(self):
        return self.renderer

    def test_view(self):
        """Create the test visualizing view."""
        self.renderer.SetBackground(0.5, 0.5, 1)
        self.create_ground()
        # self.create_wifi_signal(signal_id=0, x=0,y=0,z=0,num_arcs=3,arc_thickness=0.1,arc_resolution=50,normal=[1, 0, 0],direction=[-1, 0, 0],radius=2)
        # self.remove_wifi_signal(0)
        # self.create_building(-100, -100, 0, 50, 100)
        # self.create_building(100, 100, 0, 50, 100)
        # self.create_node(0, 0, 10)
        # self.create_node(-50, 50, 10)
        # self.create_node(50, -50, 10)
        self.renderer.GetRenderWindow().Render()

    def clear_all_packets(self):
        # Iterate through all the packet_object IDs and remove them
        for packet_id in list(self.packets.keys()):
            self.remove_packet(packet_id)

        # Render the window again to show the changes
        self.renderer.GetRenderWindow().Render()

    def clear_all_nodes(self):
        """Remove all nodes from the environment."""
        for node in self.nodes:
            node.remove_from_renderer(renderer=self.renderer)
        self.nodes = []

    def clear_all_wirelesss_packets(self):
        """Remove all wirelesss_packets from the environment."""
        # Iterate through all the packet_object IDs and remove them
        for packet_id in list(self.wireless_packets.keys()):
            self.remove_wireless_packet(packet_id)

        # Render the window again to show the changes
        self.renderer.GetRenderWindow().Render()

    def create_broadcaster_signal(self, signal_id, x, y, z, num_arcs, arc_thickness, arc_resolution,
                                  normal, direction, radius):
        # Create BroadcasterSignal example
        broadcaster_signal = BroadcasterSignal(self.renderer)
        broadcaster_signal.create_broadcaster_signal_arcs(x=x, y=y, z=z, num_arcs=num_arcs, arc_thickness=arc_thickness,
                                                          arc_resolution=arc_resolution, normal=normal,
                                                          direction=direction, radius=radius)
        self.signals[signal_id] = broadcaster_signal

    def create_wifi_signal(self, wireless_packet_id, x, y, z, num_arcs=3, arc_thickness=0.5, arc_resolution=50,
                           normal=(1, 0, 0), direction=(0, 0, 1), radius=10,
                           start_angle_azimuth=0, end_angle_azimuth=0, start_angle_elevation=0, end_angle_elevation=0):
        self.signals[wireless_packet_id] = WifiSignal(self.renderer)
        self.signals[wireless_packet_id].create_wifi_signal_arcs(x, y, z, num_arcs, arc_thickness, arc_resolution,
                                                                 normal, direction, radius,
                                                                 start_angle_azimuth, end_angle_azimuth,
                                                                 start_angle_elevation, end_angle_elevation)

    def remove_wifi_signal(self, signal_id):
        self.signals[signal_id].remove_all_arcs()
        del self.signals[signal_id]
