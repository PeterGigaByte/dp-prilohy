import customtkinter
from PIL import Image
from customtkinter import CTkProgressBar

from src.user_settings import settings


class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, container):
        super().__init__(container)

        self.simulation = None

        # open file
        self.open_button = self.init_button(settings.select_file_image(), settings.open_button_label(), 0, None)
        # start simulation
        self.start_button = self.init_button(settings.start_simulation_image(), settings.start_simulation_label(), 1,
                                             None)
        # resume simulation
        self.resume_button = self.init_button(settings.resume_simulation_image(), settings.resume_simulation_label(), 2,
                                              None)
        # pause simulation
        self.pause_button = self.init_button(settings.pause_simulation_image(), settings.pause_simulation_label(), 3,
                                             None)
        # slider which defines speed of simulation
        self.slider_button = customtkinter.CTkSlider(master=self, from_=1, to=1000, command=None)
        self.slider_button.set(500)
        self.slider_button.grid(column=4, row=0, sticky='w', padx=5, pady=8)

        #  switch which defines direction of simulation
        switch_var = customtkinter.BooleanVar(value=False)
        self.switch_button = customtkinter.CTkSwitch(master=self, text='Inverse', command=None,
                                                     variable=switch_var, onvalue=True, offvalue=False)
        self.switch_button.grid(column=5, row=0, sticky='w', padx=5, pady=8)

        # show frame
        self.grid(padx=10, pady=10, sticky=customtkinter.NSEW)

    def init_button(self, image_name, button_label, column_position, command):
        image = customtkinter.CTkImage(
            Image.open(settings.resource_path() + image_name).resize((20, 20), Image.ANTIALIAS))
        button = customtkinter.CTkButton(
            master=self,
            image=image,
            text=button_label,
            command=command
        )
        button.grid(column=column_position, row=0, sticky='w', padx=5, pady=8)
        return button


class InformationFrame(customtkinter.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(
            width=int(settings.frame_information_width()),
            height=int(settings.frame_information_height())
        )
        # progress bar definition
        self.progress_bar = CTkProgressBar(master=self, width=int(settings.bar_width()), height=30,
                                           orientation='horizontal',
                                           mode='determinate')
        self.progress_bar.set(0)
        self.progress_bar_label = customtkinter.CTkLabel(master=self, text='')

        self.grid(padx=10, pady=10, sticky=customtkinter.NSEW)

        # progress bar show

        self.progress_bar_label.grid(column=2, row=4, columnspan=30, padx=150, sticky='w')
        self.progress_bar.grid(column=0, row=3, columnspan=15, pady=5, padx=5, sticky='w')


class SimulationCanvas(customtkinter.CTkCanvas):
    def __init__(self, container):
        super().__init__(container)
        self.configure(
            width=settings.canvas_width(),
            height=settings.canvas_height(),
            background=settings.canvas_bg_color()
        )
        self.grid(padx=10, pady=10, sticky=customtkinter.W)


class Gui2D(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # init window
        self.title(settings.window_title())
        self.geometry(settings.window_size())
        self.iconbitmap(settings.resource_path() + settings.icon())
        self.resizable(False, False)
