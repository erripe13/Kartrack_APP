import customtkinter as ctk
import tkintermapview
from PIL import ImageTk, Image
import weather_mod as wm

class RaceInterface:
    def __init__(self, canvas, show_main_menu):
        self.canvas = canvas
        self.canvas.pack(fill="both", expand=True)
        self.show_main_menu = show_main_menu
        self.widgets = []

        self.entry_frame = ctk.CTkFrame(
            self.canvas,
            width=1000,
            height=900,
            corner_radius=10,
            fg_color="#191919",
            border_color="white",
            bg_color="black"
        )
        # Placer le cadre au centre de l'écran
        self.entry_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.entry_name= ctk.CTkEntry(self.entry_frame, placeholder_text="Nom du Circuit",font=("Orbitron",24))
        self.entry_name.pack(pady=10, padx=20)

        self.entry_lat = ctk.CTkEntry(self.entry_frame, placeholder_text="Latitude",font=("Orbitron",24))
        self.entry_lat.pack(pady=10, padx=20)

        self.entry_long = ctk.CTkEntry(self.entry_frame, placeholder_text="Longitude",font=("Orbitron",24))
        self.entry_long.pack(pady=10, padx=20,)


        self.entry_butt = ctk.CTkButton(
            self.entry_frame,
            width=self.entry_frame.winfo_width()-20,
            text="Valider les Coordonnées",
            command=self.display_main_interface,
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            border_color="white",
            corner_radius=10,
            font=("Orbitron", 24)
        )
        self.entry_butt.pack(pady=20,anchor="center")

        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()

        #wm.get_current_weather_conditions(self)

        self.map_frame = None
        self.time_frame = None
        self.banner = None


    def display_main_interface(self):

        # --------- Bandeau supérieur ---------
        self.banner_height = int(self.screen_height * 0.12)

        self.banner = ctk.CTkFrame(
            self.canvas,
            width=self.screen_width,
            height=self.banner_height,
            fg_color="#333333",
            bg_color="black",
            corner_radius=0
        )
        self.banner.place(x=0, y=0, anchor="nw")
        wm.display_weather(self)
        self.banner.pack(fill="x")
        self.banner.pack_propagate(False)
        self.widgets.append(self.banner)

        self.track_name_label = ctk.CTkLabel(
            self.banner,
            text=self.entry_name.get(),
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
            fg_color="#222222",
            bg_color="black"
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

        self.time_label = ctk.CTkLabel(
            self.time_frame,
            text="Temps",
            font=("Orbitron", 24),
            corner_radius=0,
            text_color="white"
        )
        self.time_label.place(relx=0.5, rely=0.1, anchor="center")
        self.widgets.append(self.time_frame)


        # --------- Bouton Retour ---------
        self.button_back = ctk.CTkButton(
            self.canvas,
            text="Menu Principal",
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

    def search_event(self, event=None):
        # Coordonnées par défaut pour Cergy
        default_lat = 49.0388
        default_long = 2.0784

        latitude_input = self.entry_lat.get()
        longitude_input = self.entry_long.get()

        latitude = latitude_input or default_lat
        longitude = longitude_input or default_long

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            latitude = default_lat
            longitude = default_long

        # Définir la position sur la map_widget
        self.map_widget.set_position(latitude, longitude, zoom=10)

        # Ajoutez d'autres informations ou styles si nécessaire

    def return_to_menu(self):
        for widget in self.widgets:
            widget.destroy()

        self.entry_frame.destroy()
        self.show_main_menu()

