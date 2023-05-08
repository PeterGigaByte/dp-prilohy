from api.rendering.rendering_objects.signal_object.signal import Signal


class WifiSignal(Signal):
    def __init__(self, renderer):
        super().__init__(renderer)
        self.arc_actors = []

    def create_wifi_signal_arcs(self, x, y, z, num_arcs=3, arc_thickness=0.5, arc_resolution=50, normal=(1, 0, 0),
                                direction=(0, 0, 1), radius=10, start_angle_azimuth=135, end_angle_azimuth=225,
                                start_angle_elevation=-45, end_angle_elevation=45):
        self.arc_actors.extend(
            self.create_signal_arcs(float(x), float(y), float(z), num_arcs, arc_thickness, arc_resolution, normal,
                                    direction, radius,
                                    start_angle_azimuth=start_angle_azimuth, end_angle_azimuth=end_angle_azimuth,
                                    start_angle_elevation=start_angle_elevation, end_angle_elevation=end_angle_elevation))

    def remove_all_arcs(self):
        for arc_actor in self.arc_actors:
            self.renderer.RemoveActor(arc_actor)
        self.arc_actors.clear()
        self.renderer.GetRenderWindow().Render()
