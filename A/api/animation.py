from PyQt5.QtCore import QCoreApplication, QTimer

from database.database import get_all_nodes, get_steps_table_size, fetch_data_from_database
from network_elements.elements import Node
from step.step_enum import StepType
from utils.calcUtils import calculate_direction
from utils.manage import get_objects_by_type, get_rendering_node_by_id


class AnimationApi:
    def __init__(self, renderer_api, bottom_dock_widget):
        self.database_remaining_len = None
        self.database_iteration_current = None
        self.database_iteration_len = None
        self.database_length = None
        self.transmission_max_step = 11
        self.wireless_packet_max_step = 19
        self.wired_packet_max_step = 19
        self.renderer_api = renderer_api
        self.bottom_dock_widget = bottom_dock_widget
        self.data = None
        self.substeps = []
        self.current_step = 0
        self.delay = 0
        self.steps_per_event = 1
        self.is_paused = False
        self.was_paused = False
        self.max_steps_callback = None
        self.steps_update_callback = None
        self.control_update_callback = None
        self.progress_bar_update_callback = None
        self.progress_bar_maximum_callback = None
        self.animation_started = False
        self.timer_step = QTimer()
        self.use_database = False
        self.animation_batch_database = 150000

    def set_data(self, data):
        self.data = data

    def set_control_update_callback(self, callback):
        self.control_update_callback = callback

    def prepare_animation(self):
        self.renderer_api.clear_all_packets()
        self.renderer_api.clear_all_nodes()
        self.renderer_api.clear_all_wirelesss_packets()
        if self.data and self.data.content or self.use_database:
            if self.use_database:
                nodes = get_all_nodes()
                self.database_length = get_steps_table_size()
                if self.database_length != 0:
                    self.database_iteration_len = self.database_length // self.animation_batch_database
                    self.database_remaining_len = self.database_length % self.animation_batch_database
                    self.control_update_callback(
                        f"Step {self.current_step} / {self.database_length}",
                        f"Time {0}",
                        self.current_step,
                        self.database_length,
                        "Animation progress:"
                    )
            else:
                nodes = get_objects_by_type(self.data.content, Node)
                self.control_update_callback(
                    f"Step {self.current_step} / {len(self.substeps)}",
                    f"Time {0}",
                    self.current_step,
                    len(self.substeps),
                    "Animation progress:"
                )
            for node in nodes:
                self.renderer_api.create_node(x=node.loc_x, y=node.loc_y, z=node.loc_z, id=node.id,
                                              description="Node " + str(node.id))
            self.renderer_api.renderer.GetRenderWindow().Render()

    def animate_substeps(self):
        if not self.animation_started:
            self.animation_started = True
            self.timer_step.timeout.connect(self.run_single_step)
            self.start_timer()

    def run_single_step(self):
        steps_executed = 0
        render_every_n_steps = 10  # Adjust this value based on your requirements

        while self.animation_should_continue():
            step = self.get_current_step()

            self.handle_step(step)
            self.current_step += 1

            self.update_control_callback(step)
            self.update_steps_callback()

            if self.should_render(steps_executed, render_every_n_steps):
                self.render_and_process_events()

            steps_executed += 1

            if self.should_break_loop(steps_executed):
                self.check_and_handle_animation_end()
                break
            self.check_and_handle_animation_end()
        self.start_timer()

    def animation_should_continue(self):
        if self.use_database:
            return self.current_step < self.database_length and not self.is_paused
        else:
            return self.current_step < len(self.substeps) and not self.is_paused

    def get_current_step(self):
        if self.use_database:
            iteration_index, step_offset = self.calculate_requested_iteration(self.current_step)
            self.fetch_data_from_database_if_necessary(iteration_index)
            step = self.substeps[step_offset]
        else:
            step = self.substeps[self.current_step]

        return step

    def fetch_data_from_database_if_necessary(self, iteration_index):
        if iteration_index != self.database_iteration_current or self.substeps is None:
            self.substeps = fetch_data_from_database(iteration_index, self.animation_batch_database)
            self.database_iteration_current = iteration_index

    def update_control_callback(self, step):
        if self.control_update_callback:
            if self.use_database:
                self.control_update_callback(
                    f"Step {self.current_step} / {self.database_length}",
                    f"Time {step.time}",
                    self.current_step,
                    self.database_length,
                    "Animation progress:"
                )
            else:
                self.control_update_callback(
                    f"Step {self.current_step} / {len(self.substeps)}",
                    f"Time {step.time}",
                    self.current_step,
                    len(self.substeps),
                    "Animation progress:"
                )

    def update_steps_callback(self):
        if self.steps_update_callback:
            self.steps_update_callback(self.current_step)

    def should_render(self, steps_executed, render_every_n_steps):
        return steps_executed % render_every_n_steps == 0

    def render_and_process_events(self):
        self.renderer_api.renderer.GetRenderWindow().Render()
        QCoreApplication.processEvents()  # Process events during animation

    def should_break_loop(self, steps_executed):
        return steps_executed >= self.steps_per_event

    def check_and_handle_animation_end(self):
        if self.current_step == self.database_length:
            self.bottom_dock_widget.log("Animation finished (using database).")
        elif not self.use_database and self.current_step == len(self.substeps):
            self.bottom_dock_widget.log("Animation finished.")

    def handle_step(self, step):
        match step.type:
            case StepType.WIRED_PACKET:
                self.handle_packet_step(step)
            case StepType.NODE_UPDATE:
                self.handle_node_update(step)
            case StepType.BROADCAST:
                self.handle_broadcast(step)
            case StepType.WIRELESS_PACKET_RECEPTION:
                self.handle_wireless_packet_reception(step)

    def handle_node_update(self, step):
        # Find the node_object with the matching ID
        node = get_rendering_node_by_id(self.renderer_api.nodes, step.node_id)
        node.update_attributes(step, self.renderer_api.renderer)

    def handle_broadcast(self, step):
        broadcast_id = step.broadcast_id
        x, y, z = float(step.loc_x), float(step.loc_y), float(step.loc_z)
        normal = (1, 0, 0)
        direction = calculate_direction(normal)
        if step.step_number == 0:
            self.renderer_api.create_broadcaster_signal(signal_id=broadcast_id, x=x, y=y, z=z,
                                                        num_arcs=1, radius=step.radius, arc_thickness=0.5,
                                                        arc_resolution=50, normal=normal, direction=direction)
        elif step.step_number == self.transmission_max_step and broadcast_id in self.renderer_api.signals:
            if broadcast_id in self.renderer_api.signals:
                self.renderer_api.remove_wifi_signal(broadcast_id)
        # Update the position of the packet_object for intermediate steps
        elif broadcast_id in self.renderer_api.signals:
            self.renderer_api.remove_wifi_signal(broadcast_id)
            self.renderer_api.create_broadcaster_signal(signal_id=broadcast_id, x=x, y=y, z=z,
                                                        num_arcs=1, radius=step.radius, arc_thickness=0.5,
                                                        arc_resolution=50, normal=normal, direction=direction)

    def handle_packet_step(self, step):
        packet_id = step.packet_id
        x, y, z = float(step.loc_x), float(step.loc_y), float(step.loc_z)
        if step.step_number == 0:
            self.renderer_api.create_packet(x, y, z, packet_id=packet_id)
            if step.meta_info:
                self.bottom_dock_widget.log(step.meta_info)
        elif step.step_number == self.wired_packet_max_step and packet_id in self.renderer_api.packets:
            if packet_id in self.renderer_api.packets:
                self.renderer_api.remove_packet(packet_id)
        # Update the position of the packet_object for intermediate steps
        elif packet_id in self.renderer_api.packets:
            self.renderer_api.update_packet_position(packet_id, x, y, z)

    def handle_wireless_packet_reception(self, step):
        wireless_packet_id = step.packet_id
        x, y, z = step.loc_x, step.loc_y, step.loc_z

        # Add the wireless packet to the renderer for the first step
        if step.step_number == 0:
            self.renderer_api.create_wireless_packet(x, y, z, packet_id=wireless_packet_id)
            if step.meta_info:
                self.bottom_dock_widget.log(step.meta_info)
        # Remove the wireless packet from the renderer for the last step
        elif step.step_number == self.wireless_packet_max_step and wireless_packet_id in self.renderer_api.wireless_packets:
            self.renderer_api.remove_wireless_packet(wireless_packet_id)

        # Update the position of the donut_object for intermediate steps
        elif wireless_packet_id in self.renderer_api.wireless_packets:
            self.renderer_api.update_wireless_packet_position(wireless_packet_id, x, y, z)

    def start_timer(self):
        self.timer_step.start(self.delay)

    def stop_timer(self):
        self.timer_step.stop()

    def pause_unpause_animation(self):
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.start_timer()
        else:
            self.stop_timer()

    def pause_animation(self):
        self.was_paused = self.is_paused
        self.is_paused = True
        self.stop_timer()

    def unpause_animation(self):
        self.is_paused = False
        self.start_timer()

    def reset_animation(self):
        self.current_step = 0
        self.steps_per_event = 1
        self.clear_vtk_window()

    def clear_vtk_window(self):
        if self.use_database:
            if self.current_step == 0:
                substeps_size = 9999
                time = 0
            else:
                iteration_index, step_offset = self.calculate_requested_iteration(self.current_step)
                self.fetch_data_from_database_if_necessary(iteration_index)
                substeps_size = len(self.substeps)
                time = self.substeps[step_offset].time
        else:
            if len(self.substeps) == 0:
                substeps_size = 9999
                time = 0
            elif len(self.substeps) == self.current_step:
                substeps_size = len(self.substeps)
                time = self.substeps[len(self.substeps) - 1].time
            else:
                substeps_size = len(self.substeps)
                time = self.substeps[self.current_step].time

        self.prepare_animation()

        if self.control_update_callback:
            self.control_update_callback(f"Step {self.current_step} / {len(self.substeps)}", f"Time {time}",
                                         self.current_step, substeps_size, "Animation progress:")

    def update_delay(self, new_delay):
        self.delay = new_delay

    def update_steps_per_event(self, new_steps_per_event):
        self.steps_per_event = new_steps_per_event

    def set_update_steps_callback(self, callback):
        self.steps_update_callback = callback

    def set_current_step(self, new_step):
        self.current_step = new_step
        self.clear_vtk_window()

        for i in range(new_step):
            self.control_update_callback(
                f"Step {i} / {new_step}",
                f"Time {0}",
                i,
                new_step,
                "Getting ready for animation:"
            )
            if self.use_database:
                iteration_index, step_offset = self.calculate_requested_iteration(i)
                self.fetch_data_from_database_if_necessary(iteration_index)
                step = self.substeps[step_offset]
            else:
                if i < len(self.substeps):
                    step = self.substeps[i]
                else:
                    break

            if step.type == StepType.NODE_UPDATE:
                self.handle_node_update(step)
            elif step.type == StepType.WIRED_PACKET and i >= (new_step - 100):
                self.handle_packet_step(step)
            elif step.type == StepType.WIRELESS_PACKET_RECEPTION and i >= (new_step - 100):
                self.handle_wireless_packet_reception(step)

    def set_max_steps_callback(self, callback):
        self.max_steps_callback = callback

    def update_steps_constants(self, wired_packet_max_step, wireless_packet_max_step, transmission_max_step,
                               use_database, animation_batch):
        self.wired_packet_max_step = wired_packet_max_step - 1
        self.wireless_packet_max_step = wireless_packet_max_step - 1
        self.transmission_max_step = transmission_max_step - 1
        self.use_database = use_database
        self.animation_batch_database = animation_batch

    def set_substeps(self, substeps):
        self.substeps = substeps
        if self.max_steps_callback:
            if self.use_database:
                self.max_steps_callback(self.database_length)
            else:
                self.max_steps_callback(len(self.substeps))

    def calculate_requested_iteration(self, step):
        if step >= self.database_length:
            step = self.database_length - 1

        # Calculate the requested iteration
        iteration_index = step // self.animation_batch_database

        # Calculate the step offset within the current iteration
        step_offset = step % self.animation_batch_database

        return iteration_index, step_offset



