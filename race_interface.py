import customtkinter
import customtkinter as ctk
import tkintermapview
from PIL import ImageTk, Image
import tkinter as tk

class RaceInterface:
    def __init__(self, canvas, show_main_menu):
        self.canvas = canvas
        self.canvas.pack(fill="both", expand=True)
        self.show_main_menu = show_main_menu
        self.widgets = []

        self.entry_frame = ctk.CTkFrame(
            self.canvas,
            width=500,  # Largeur du cadre (par exemple, 500 pixels)
            height=300,  # Hauteur du cadre (par exemple, 300 pixels)
            corner_radius=10,
            fg_color="#222222"
        )
        # Placer le cadre au centre de l'écran
        self.entry_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.entry_lat = ctk.CTkEntry(self.entry_frame, placeholder_text="Latitude",font=("Orbitron",24))
        self.entry_lat.pack(pady=10, padx=20)

        self.entry_long = ctk.CTkEntry(self.entry_frame, placeholder_text="Longitude",font=("Orbitron",24))
        self.entry_long.pack(pady=10, padx=20,)


        self.entry_butt = ctk.CTkButton(
            self.entry_frame,
            text="Valider les Coordonnées",
            command=self.display_main_interface,
            font=("Orbitron", 24)
        )
        self.entry_butt.pack(pady=20)

        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()

        self.map_frame = None
        self.time_frame = None
        self.banner = None


    def display_main_interface(self):
        # --------- Bandeau supérieur ---------
        self.banner_height = int(self.screen_height * 0.1)

        self.banner = ctk.CTkFrame(
            self.canvas,
            width=self.screen_width,
            height=self.banner_height,
            fg_color="#333333",
            corner_radius=0
        )
        self.banner.place(x=0, y=0, anchor="nw")
        self.widgets.append(self.banner)

        self.track_name_label = ctk.CTkLabel(
            self.banner,
            text="Nom du Circuit",
            font=("Orbitron", 24),
            corner_radius=0,
            text_color="white"
        )
        self.track_name_label.place(relx=0.1, rely=0.5, anchor="center")
        self.widgets.append(self.track_name_label)

        # --------- Image satellite à gauche (2/3) ---------
        left_width = int(self.screen_width * 2 / 3)
        left_height = self.screen_height - self.banner_height

        self.map_frame = ctk.CTkFrame(
            self.canvas,
            width=left_width,
            height=left_height,
            corner_radius=0,
            fg_color="#222222"
        )
        self.map_frame.place(x=0, y=self.banner_height)
        self.widgets.append(self.map_frame)
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame,width=(left_width-40),height=(left_height-50))
        self.map_widget.place(relx=0.5, rely=0.5, anchor="center")
        self.search_event()


        # --------- Chronos à droite (1/3) ---------
        right_width = self.screen_width - left_width
        right_height = self.screen_height - self.banner_height

        self.time_frame = ctk.CTkFrame(
            self.canvas,
            width=right_width,
            height=right_height,
            corner_radius=0,
            fg_color="#1A1D21"
        )
        self.time_frame.place(x=left_width, y=self.banner_height, anchor="nw")
        self.widgets.append(self.time_frame)

        # --------- Bouton Retour ---------
        self.button_back = ctk.CTkButton(
            self.canvas,
            text="Retour au Menu Principal",
            command=self.return_to_menu,
            width=right_width,
            height=50,
            border_width=3,
            border_color="#191919",
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            corner_radius=10,
            text_color="white",
            font=("Orbitron", 16)
        )
        self.button_back.place(x=left_width, y=self.screen_height-50,anchor="nw")
        self.widgets.append(self.button_back)

        print("Interface Kartrack LIVE affichée !")

    def search_event(self, event=None):
        self.map_widget.set_position(float(self.entry_lat.get()), float(self.entry_long.get()))

    def return_to_menu(self):
        for widget in self.widgets:
            widget.destroy()

        self.entry_frame.destroy()
        self.show_main_menu()