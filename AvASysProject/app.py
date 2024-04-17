from src.CTkMessagebox import CTkMessagebox
import tkintermapview
from PIL import Image, ImageTk
import customtkinter
import tkinter as tk
from tkinter import ttk
import os
import gps
import serialCom


class MainScreen(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ---------------------------------------- Serial Config
        self.portManager = serialCom.COM()
        self.openPorts = self.portManager.getSerialPorts()
        self.bauds = ["300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "31250", "38400",
                      "57600", "115200"]

        # ---------------------------------------- App Config
        self.title("Neo Stellar AvaSys V1.0")

        # ---------------------------------------- Geometry Variables
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        screenx = self.screen_width - 20
        screeny = self.screen_height - 100

        # ---------------------------------------- Geometry Shifting
        x = (self.screen_width - screenx) // 2
        y = (self.screen_height - screeny) // 2

        # ---------------------------------------- Window Settings
        self.geometry(f"{screenx}x{screeny}+{x}+{y - 35}")
        self.resizable(False, False)

        # ---------------------------------------- Grid Define

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)

        # ---------------------------------------- Frame Define

        upbar = customtkinter.CTkFrame(self)
        upbar.grid(row=0, column=0, sticky="nsew")

        infoFrame = customtkinter.CTkFrame(self)
        infoFrame.grid(row=1, column=0, sticky="nsew")

        bigScreen = customtkinter.CTkFrame(self, )  # Sağda kalan büyük iki rowluk alan
        bigScreen.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Big Area Row Conf
        bigScreen.columnconfigure(0, weight=1)
        bigScreen.rowconfigure(0, minsize=75)
        bigScreen.rowconfigure(1, weight=160)
        bigScreen.rowconfigure(2, weight=1)

        # Big Area Grids
        subframe_upperbar = customtkinter.CTkFrame(bigScreen)
        subframe_upperbar.grid(row=0, column=0, sticky="nsew", pady=0)

        subframe_map = customtkinter.CTkFrame(bigScreen)
        subframe_map.grid(row=1, column=0, sticky="nsew")

        subframe_log = customtkinter.CTkFrame(bigScreen)
        subframe_log.grid(row=2, column=0, sticky="nsew")

        # NavBar Grids
        subframe_upperbar.columnconfigure(0, weight=1)
        subframe_upperbar.columnconfigure(1, weight=1)
        subframe_upperbar.columnconfigure(2, weight=1)
        subframe_upperbar.columnconfigure(3, weight=1)
        subframe_upperbar.columnconfigure(4, weight=1)
        subframe_upperbar.columnconfigure(5, weight=4)

        # Navbar Sub frames
        mainScreenButtonFrame = customtkinter.CTkFrame(subframe_upperbar)
        mainScreenButtonFrame.grid(row=0, column=0, sticky="nsew")

        dataButtonFrame = customtkinter.CTkFrame(subframe_upperbar)
        dataButtonFrame.grid(row=0, column=1, sticky="nsew")

        setupButtonFrame = customtkinter.CTkFrame(subframe_upperbar)
        setupButtonFrame.grid(row=0, column=2, sticky="nsew")

        configButtonFrame = customtkinter.CTkFrame(subframe_upperbar)
        configButtonFrame.grid(row=0, column=3, sticky="nsew")

        helpButtonFrame = customtkinter.CTkFrame(subframe_upperbar)
        helpButtonFrame.grid(row=0, column=4, sticky="nsew")

        connectFrame = customtkinter.CTkFrame(subframe_upperbar)
        connectFrame.grid(row=0, column=5, sticky="nsew")

        # Connection Grids
        connectFrame.columnconfigure(0, weight=1)
        connectFrame.columnconfigure(1, weight=1)
        connectFrame.columnconfigure(2, weight=1)
        connectFrame.rowconfigure(0, weight=1)
        connectFrame.rowconfigure(1, weight=1)

        # Calls all pending idle tasks, without processing any other events. This can be used to carry out geometry
        # management and redraw widgets if necessary, without calling any callbacks.
        self.update_idletasks()

        # ---------------------------------------- Commands

        def getPortFromCombo(event):
            self.portManager.setSerialPort(event)
            self.port = event

        def getBaudFromCombo(event):
            self.portManager.setBaudRate(event)
            self.baud = int(event)

        def connectSerial():
            if connectButton.cget('text') == "Connect":
                if not (self.portManager.getSerialPort() is None or self.portManager.getBaudRate() is None):
                    if self.portManager.start_reading(console_log):
                        connectButton.configure(text="Disconnect")
                else:
                    CTkMessagebox(title="Port Error", message="Seral Port(COM) or Baudrate(Serial) can't be empty!")
            else:
                if self.portManager.stop_reading(console_log):
                    CTkMessagebox(message="Başlantı başarılı bir şekilde kapatıldı!",
                                  icon="check", option_1="Tamam")
                    connectButton.configure(text="Connect")
                else:
                    CTkMessagebox(title="Error", message="Bağlantı sonlandırılırken bir hata gerçekleşti",
                                  icon="cancel")

        # ---------------------------------------- Widgets
        mainScreenButton = customtkinter.CTkButton(mainScreenButtonFrame, text="Main Screen")
        mainScreenButton.pack(expand=True, fill='both')

        dataButton = customtkinter.CTkButton(dataButtonFrame, text="Flight Data")
        dataButton.pack(expand=True, fill='both')

        setupButton = customtkinter.CTkButton(setupButtonFrame, text="Setup")
        setupButton.pack(expand=True, fill='both')

        configButton = customtkinter.CTkButton(configButtonFrame, text="Config")
        configButton.pack(expand=True, fill='both')

        helpButton = customtkinter.CTkButton(helpButtonFrame, text="Help")
        helpButton.pack(expand=True, fill='both')

        connectionPortLabel = customtkinter.CTkLabel(connectFrame, text="COM: ")
        connectionPortLabel.grid(row=0, column=0, sticky="e")
        connectPort = customtkinter.CTkComboBox(connectFrame, values=self.openPorts, command=getPortFromCombo)
        connectPort.grid(row=0, column=1, sticky="w")

        connectionSerialRate = customtkinter.CTkLabel(connectFrame, text="Serial: ")
        connectionSerialRate.grid(row=1, column=0, sticky="e")
        connectSerialRate = customtkinter.CTkComboBox(connectFrame, values=self.bauds, command=getBaudFromCombo)
        connectSerialRate.grid(row=1, column=1, sticky="w")

        connectButton = customtkinter.CTkButton(connectFrame, text="Connect", command=connectSerial)
        connectButton.grid(row=0, column=3, rowspan=2, sticky="nswe")

        alt_img = customtkinter.CTkImage(Image.open("src/new1.png"), size=(upbar.winfo_width(), upbar.winfo_height()))
        altitudeGauge = customtkinter.CTkLabel(upbar, image=alt_img)
        altitudeGauge.pack(expand=True, fill='both')

        print(subframe_map.winfo_height())

        map_widget = tkintermapview.TkinterMapView(subframe_map, width=int(1600),
                                                   height=int(890), corner_radius=10)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        loc_data = gps.GPSModule().getMyLoc()
        plane_image = ImageTk.PhotoImage(Image.open("src/plane.png").resize((40, 40)))
        map_widget.set_marker(float(loc_data[0]), float(loc_data[1]), icon=plane_image)
        map_widget.set_position(float(loc_data[0]), float(loc_data[1]))
        map_widget.pack()

        console_log = customtkinter.CTkTextbox(subframe_log, width=1600, corner_radius=0)
        console_log.grid(row=0, column=0, sticky="nsew")
        console_log.insert("0.0", "Güncelleme bulunmadı.")
        console_log.configure(state="disabled")
        """denememm**************************************************************************************************"""

        def open_setup_page():
            # Hide the map frame
            subframe_map.destroy()

            # Show the setup page
            setup_page_frame = customtkinter.CTkFrame(bigScreen)
            setup_page_frame.grid(row=1, column=0, sticky="nsew")
            setup_page_frame.pack(expand=True, fill='both')
            label = customtkinter.CTkLabel(setup_page_frame, text="This is the Setup Page")
            setup_page_frame.lift()
            label.pack()

        def open_data_page():
            # Hide the map frame
            subframe_map.destroy()

            # Show the data page
            data_page_frame = customtkinter.CTkFrame(bigScreen)
            data_page_frame.grid(row=1, column=0, sticky="nsew")
            data_page_frame.pack(expand=True, fill='both')

        # Configure the setup button
        setupButton.configure(command=open_setup_page)

        # Configure the data button
        dataButton.configure(command=open_data_page)

        def open_page():
            self.map_frame = customtkinter.CTkFrame(subframe_map)
            self.map_frame.pack(expand=True, fill='both')

            # Add the content to the map frame
            self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=int(1600),
                                                            height=int(890), corner_radius=10)
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
            loc_data = gps.GPSModule().getMyLoc()
            plane_image = ImageTk.PhotoImage(Image.open("src/plane.png").resize((40, 40)))
            self.map_widget.set_marker(float(loc_data[0]), float(loc_data[1]), icon=plane_image)
            self.map_widget.set_position(float(loc_data[0]), float(loc_data[1]))
            self.map_widget.pack()

        mainScreenButton.configure(command=open_page)

        # ---------------------------------------- Handling Closing

        def close_window():
            self.quit()

        self.protocol("WM_DELETE_WINDOW", close_window)

class LoginScreen(customtkinter.CTk):
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.isAttempted = False
        self.geometry(f"{400}x{600}")
        self.title("Neo Stellar Ground Controller v1.0b")
        self.resizable(False, False)

        def get_input():
            user_input = login_name.get()
            user_pass = login_password.get()

            if user_input == "admin" and user_pass == "admin":
                print("Login Success")
                print(f"{user_input}, {user_pass}")
                open_main_screen(self)
                self.withdraw()
            else:
                if not self.isAttempted:
                    error_label = customtkinter.CTkLabel(self, text="Invalid Username / Password", text_color="red")
                    error_label.pack()
                    self.isAttempted = True

        def open_main_screen(window):
            if window.toplevel_window is None or not window.toplevel_window.winfo_exists():
                window.toplevel_window = MainScreen(window)  # create window if its None or destroyed
            else:
                window.toplevel_window.focus()  # if window exists focus it

        self.toplevel_window = None

        img = customtkinter.CTkImage(light_image=Image.open("src/login_icon.png"), size=(60, 60))
        image_label = customtkinter.CTkLabel(self, image=img, text="")
        image_label.pack()

        login_name = customtkinter.CTkEntry(self)
        login_name.pack()

        login_password = customtkinter.CTkEntry(self, show="*")
        login_password.pack()

        login_button = customtkinter.CTkButton(self, text="Login", command=get_input)
        login_button.pack()