import copy
import datetime
import time
import uuid

from PyQt5.QtCore import pyqtSignal, QThread
from tqdm import tqdm

from database.database import insert_node_updates_to_steps, get_all_nodes, \
    update_wireless_packet_reception_fb_tx, clear_steps, insert_steps_to_database, get_data, get_data_length
from network_elements.elements import WiredPacket, Node, NodeUpdate, WirelessPacketReception, Broadcaster
from step.step import WiredPacketStep, NodeUpdateStep, WirelessPacketReceptionStep
from step.step_enum import StepType, NodeUpdateType
from utils.calcUtils import interpolate_coordinates_3D
from utils.manage import get_objects_by_type


class StepProcessor(QThread):
    data_processed = pyqtSignal(object)
    update_status = pyqtSignal(int, int, float, str)

    def __init__(self, bottom_dock_widget):

        super().__init__()
        self.data = None
        self.node_dict = None
        self.batch_size = 1500000
        self.database_batch_size = 1500000
        self.bottom_dock_widget = bottom_dock_widget
        self.step_types = StepType
        self.substeps = {step_type: [] for step_type in self.step_types}
        # Set the number of steps to interpolate between each substep for wired packets
        self.num_steps_wired_packet_animation = 20
        # broadcast step parameters
        self.num_steps_broadcast_transmission = 12
        # wireless packet_object reception step parameters
        self.num_steps_wireless_packet_reception = 20
        # first radius
        self.radius_constant = 2
        self.end_time_constant = 0.000010
        self.optimized_parser = False

    def run(self):
        result = None
        if self.data is not None:
            self.data = self.data.content
        if self.optimized_parser:
            self.process_steps_with_sql_calls()
        else:
            result = self.process_steps_without_sql_calls(self.data)
        self.data_processed.emit(result)

    def process_steps_with_sql_calls(self):
        # Insert the processed data into the steps table
        # Define the query

        clear_steps()
        self.process_node_update()
        self.update_wireless_packet_reception()
        self.process_optimised_data()
        # Close the database connection

    def process_steps_without_sql_calls(self, data, node_data=None):
        """
        Processes the animation steps for the provided data and returns a sorted list of all substeps.

        Args:
        - data: an object containing the data to process

        Returns:
        - A sorted list of all substeps for the provided data
        """
        self.bottom_dock_widget.log("Processing of steps begin.")
        # Get the node_object data, node_object update data, and wired packet_object data from the content of the
        # provided data
        if not self.optimized_parser and node_data is None:
            node_data = get_objects_by_type(data, Node)
        node_update_data = get_objects_by_type(data, NodeUpdate)
        wired_packet_data = get_objects_by_type(data, WiredPacket)
        broadcaster_data = get_objects_by_type(data, Broadcaster)
        wireless_packet_data = get_objects_by_type(data, WirelessPacketReception)

        """If changed - do not forget to update in animation handlers!!"""

        """-----------------------------------------------------------"""
        # Combine the node_object update data and wired packet_object data
        combined_data = node_update_data + wired_packet_data + broadcaster_data + wireless_packet_data

        self.bottom_dock_widget.log("Processing of steps before sorting.")
        # Sort the combined data by time
        combined_data.sort(key=sorting_key)

        # Create a copy of the node_object data to update
        updated_node_data = copy.deepcopy(node_data)
        wireless_packet_max_time_map = {}

        for item in wireless_packet_data:
            if item.unique_id not in wireless_packet_max_time_map or item.first_byte_received_time \
                    > wireless_packet_max_time_map[item.unique_id]:
                wireless_packet_max_time_map[item.unique_id] = item.first_byte_received_time
        broadcaster_transmitted = {}
        # Loop through the combined data and generate substeps for each item
        for item in combined_data:
            if isinstance(item, NodeUpdate):
                # If the item is a NodeUpdate, update the position of the corresponding node_object and add a
                # NodeUpdateStep Find the node_object with the matching ID in updated_node_data
                node = next((node for node in updated_node_data if node.id == item.id), None)

                # If the node_object exists, update its position
                if node:
                    if item.x and item.y and item.z is not None:
                        node.loc_x, node.loc_y, node.loc_z = item.x, item.y, item.z

                self.update_node_position(item)
            elif isinstance(item, WiredPacket):
                # If the item is a WiredPacket, generate substeps for the packet_object and add WiredPacketStep objects
                self.generate_wired_packet_substeps(self.num_steps_wired_packet_animation,
                                                    item.first_byte_transmission_time,
                                                    item.first_byte_received_time, updated_node_data[int(item.from_id)],
                                                    updated_node_data[int(item.to_id)],
                                                    item.meta_info, True)

            elif isinstance(item, Broadcaster):
                broadcaster_transmitted[item.unique_id] = item
            elif isinstance(item, WirelessPacketReception):
                # If the item is a WirelessPacketReception, do nothing (for now)
                self.generate_wired_packet_substeps(self.num_steps_wireless_packet_reception,
                                                    broadcaster_transmitted[
                                                        item.unique_id].first_byte_transmission_time,
                                                    item.first_byte_received_time,
                                                    updated_node_data[
                                                        int(broadcaster_transmitted[item.unique_id].from_id)],
                                                    updated_node_data[int(item.to_id)])

        # Combine all substeps for each step type and sort them by time
        all_substeps = []
        for step_type_list in self.substeps.values():
            all_substeps.extend(step_type_list)
        all_substeps.sort(key=lambda x: x.time)
        self.bottom_dock_widget.log("Processing of steps after sorting.")
        self.bottom_dock_widget.log("Processing of steps end.")
        return all_substeps

    def display_steps(self):
        """
        Displays the substeps in the substeps dictionary in sorted order, with a delay between each step.

        Args:
        - None

        Returns:
        - None
        """
        # Set the duration of each step to 0.5 seconds
        step_duration = datetime.timedelta(seconds=0.5)

        # Combine all substeps for each step type and sort them by time
        all_substeps = []
        for step_type_list in self.substeps.values():
            all_substeps.extend(step_type_list)
        all_substeps.sort(key=lambda x: x.time)

        # Loop through each substep and print its information with a delay between steps
        for substep in all_substeps:
            print(f"Time: {substep.time}")

            if isinstance(substep, WiredPacketStep):
                # If the substep is a WiredPacketStep, print its information
                print(
                    f"  packetId: {substep.packet_id} fId: {substep.from_id} tId: {substep.to_id} fbTx: {substep.first_byte_transmission_time} fbRx: {substep.first_byte_received_time}")
                print(f"  step_n: {substep.step_number}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")
                print(f"  Meta-info: {substep.meta_info}")
            elif isinstance(substep, NodeUpdateStep) and False:
                # If the substep is a NodeUpdateStep, print its information
                print(f"  node_id: {substep.node_id}")
                print(f"  r: {substep.red} g: {substep.green} b: {substep.blue}")
                print(f"  w: {substep.width} h: {substep.height}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")
                print(f"  description: {substep.description}")
            elif isinstance(substep, WirelessPacketReceptionStep):
                # If the substep is a NodeUpdateStep, print its information
                print(f"  wireless_packet_id: {substep.packet_id}")
                print(f"  step number: {substep.step_number} fId: {substep.from_id} tId: {substep.to_id}")
                print(f"  x: {substep.loc_x} y: {substep.loc_y} z: {substep.loc_z}")

            print()

            # Delay for the duration of a step
            time.sleep(step_duration.total_seconds())

    def generate_wired_packet_substeps(self, num_steps, start_time,
                                       end_time, from_node, to_node, meta_info="",
                                       is_wired=False):
        if to_node is None:
            to_id = -1
        else:
            to_id = to_node.id
        # Generate a unique packet_object ID
        packet_id = uuid.uuid4()

        # Calculate the total time difference between transmission and reception
        time_difference = float(end_time) - float(start_time)

        # Loop through the number of steps specified
        for step in range(num_steps):
            # Calculate the time step based on the transmission and reception times
            time_step = float(start_time) + (
                    step * time_difference / (num_steps - 1))

            # Get the source and destination node coordinates at the current time step
            src_x, src_y, src_z = (from_node.loc_x, from_node.loc_y, from_node.loc_z)

            if to_node is None:
                drop_packet_constant = (5 * step)
                dst_x, dst_y, dst_z = (src_x + drop_packet_constant, src_y + drop_packet_constant, src_z + drop_packet_constant)
            else:
                dst_x, dst_y, dst_z = (to_node.loc_x, to_node.loc_y, to_node.loc_z)

            # Interpolate the 3D coordinates between the source and destination nodes
            x, y, z = interpolate_coordinates_3D((float(src_x), float(src_y), float(src_z)),
                                                 (float(dst_x), float(dst_y), float(dst_z)), step, num_steps)

            if is_wired:
                # Create a WiredPacketStep object for this substep
                data = WiredPacketStep(time_step, packet_id, from_node.id, to_id,
                                       float(start_time), float(end_time),
                                       meta_info, step, x, y, z)
            else:
                # Create a WiredPacketStep object for this substep
                data = WirelessPacketReceptionStep(time_step, packet_id, from_node.id, to_id,
                                                   float(start_time), float(end_time),
                                                   step, x, y, z, meta_info)

            # Append the WiredPacketStep object to the list of substeps
            if data.from_id != data.to_id and is_wired:
                self.substeps[StepType.WIRED_PACKET].append(data)
            elif data.from_id != data.to_id:
                self.substeps[StepType.WIRELESS_PACKET_RECEPTION].append(data)

    def update_node_position(self, item):
        """
        Updates the position of a node_object in updated_node_data and adds a NodeUpdateStep to the substeps.

        Args:
        - item: an object representing the updated node_object position
        - updated_node_data: a dictionary containing updated node_object data

        Returns:
        - None
        """

        # Create a NodeUpdateStep object for this update
        node_update = NodeUpdateStep(time=float(item.time), update_type=NodeUpdateType[item.p.upper()], node_id=item.id,
                                     red=item.r, green=item.g, blue=item.b,
                                     width=item.w, height=item.h,
                                     loc_x=item.x, loc_y=item.y, loc_z=item.z, description=item.descr)

        # Append the NodeUpdateStep object to the list of substeps
        self.substeps[StepType.NODE_UPDATE].append(node_update)

    def update_constants(self, batch_size, database_batch_size, num_steps_wired_packet_animation,
                         num_steps_broadcast_transmission,
                         num_steps_wireless_packet_reception, radius_constant, end_time_constant, optimized_parser):
        self.batch_size = batch_size
        self.database_batch_size = database_batch_size
        self.num_steps_wired_packet_animation = num_steps_wired_packet_animation
        self.num_steps_broadcast_transmission = num_steps_broadcast_transmission
        self.num_steps_wireless_packet_reception = num_steps_wireless_packet_reception
        self.radius_constant = radius_constant
        self.end_time_constant = end_time_constant
        self.optimized_parser = optimized_parser

    def process_node_update(self):
        self.bottom_dock_widget.log("Process of nodes update started.")
        insert_node_updates_to_steps()
        self.bottom_dock_widget.log("Process of node update ended.")

    def update_wireless_packet_reception(self):
        self.bottom_dock_widget.log("Process of updating wireless packet reception started.")
        update_wireless_packet_reception_fb_tx()
        self.bottom_dock_widget.log("Process of updating wireless packet reception ended.")


    def process_data(self, data):
        match data:
            case NodeUpdate():
                if data.p == 'p':
                    self.node_dict.get(data.id).set_coordinates(data.x, data.y, data.z)
            case WiredPacket():
                self.generate_wired_packet_substeps(self.num_steps_wired_packet_animation,
                                                    data.first_byte_transmission_time, data.first_byte_received_time,
                                                    self.node_dict.get(data.from_id), self.node_dict.get(data.to_id),
                                                    data.meta_info, True)
            case WirelessPacketReception():
                self.generate_wired_packet_substeps(self.num_steps_wireless_packet_reception,
                                                    data.first_byte_transmission_time,
                                                    data.first_byte_received_time, self.node_dict.get(data.from_id),
                                                    self.node_dict.get(data.to_id), data.meta_info)


    def process_optimised_data(self):
        self.node_dict = {node.id: node for node in get_all_nodes()}
        length = get_data_length()
        offset = 0

        # Initialize substeps dictionary
        substeps = {
            StepType.WIRED_PACKET: [],
            StepType.WIRELESS_PACKET_RECEPTION: []
        }
        t1_start = time.perf_counter()
        while offset < length:
            merged_data = get_data(offset, self.batch_size)
            data_length = len(merged_data)

            substeps_length = 0

            for idx, data in enumerate(tqdm(merged_data, total=data_length)):
                self.process_data(data)
                time_elapsed = float(time.perf_counter() - t1_start)

                self.update_status.emit(offset + idx + 1, length, time_elapsed, "Step processing:")

                # Check if any substeps were generated during the processing
                for step_type in substeps:
                    substeps[step_type].extend(self.substeps[step_type])
                    substeps_length += len(self.substeps[step_type])
                    self.substeps[step_type] = []

                # Save data to the database and clear the list when the desired length is reached
                if substeps_length >= self.batch_size:
                    for step_type in substeps:
                        if len(substeps[step_type]) != 0:
                            insert_steps_to_database(substeps[step_type],
                                                     1 if step_type == StepType.WIRED_PACKET else 3, self.database_batch_size)
                            substeps[step_type] = []
                    substeps_length = 0

            # Update the offset
            offset += data_length

        # Save any remaining data to the database
        for step_type in substeps:
            if len(substeps[step_type]) != 0:
                insert_steps_to_database(substeps[step_type], 1 if step_type == StepType.WIRED_PACKET else 3, self.database_batch_size)

        self.bottom_dock_widget.log("Processing finished.")


def sorting_key(x):
    if hasattr(x, 'time') and x.time is not None:
        return float(x.time)
    elif hasattr(x, 'first_byte_transmission_time') and x.first_byte_transmission_time is not None:
        return float(x.first_byte_transmission_time)
    elif x.first_byte_received_time is not None:
        return float(x.first_byte_received_time)
    else:
        return 0


