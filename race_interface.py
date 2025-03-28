import customtkinter as ctk
from PIL import ImageTk, Image
import tkinter as tk

class RaceInterface:
    def __init__(self, canvas, show_main_menu):
        self.canvas = canvas
        self.show_main_menu = show_main_menu
        self.widgets = []

        # Récupère la taille de l'écran
        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()

        # --------- Bandeau supérieur ---------
        self.banner_height = int(self.screen_height * 0.1)

        self.banner = ctk.CTkFrame(
            self.canvas,
            width=self.screen_width,
            height=self.banner_height,
            fg_color="#333333"
        )
        self.banner.place(x=0, y=0)
        self.widgets.append(self.banner)

        self.track_name_label = ctk.CTkLabel(
            self.banner,
            text="Nom du Circuit",
            font=("Orbitron", 24),
            text_color="white"
        )
        self.track_name_label.place(relx=0.5, rely=0.5, anchor="center")
        self.widgets.append(self.track_name_label)

        # --------- Image satellite à gauche (2/3) ---------
        left_width = int(self.screen_width * 2 / 3)
        left_height = self.screen_height - self.banner_height

        self.image_frame = ctk.CTkFrame(
            self.canvas,
            width=left_width,
            height=left_height,
            fg_color="#222222"
        )
        self.image_frame.place(x=0, y=self.banner_height)
        self.widgets.append(self.image_frame)

        # Image fictive (à remplacer par une vraie image satellite)
        try:
            image = Image.open("circuit_satellite.jpg")  # mets le chemin de ton image
            image = image.resize((left_width, left_height))
            self.image_sat = ImageTk.PhotoImage(image)

            self.image_label = ctk.CTkLabel(self.image_frame, image=self.image_sat, text="")
            self.image_label.pack(fill="both", expand=True)
            self.widgets.append(self.image_label)
        except Exception as e:
            print("Image non chargée :", e)

        # --------- Chronos à droite (1/3) ---------
        right_width = self.screen_width - left_width
        right_height = left_height

        self.time_frame = ctk.CTkFrame(
            self.canvas,
            width=right_width,
            height=right_height,
            fg_color="#1A1D21"
        )
        self.time_frame.place(x=left_width, y=self.banner_height)
        self.widgets.append(self.time_frame)

        self.time_label = ctk.CTkLabel(
            self.time_frame,
            text="Chronos",
            font=("Orbitron", 20),
            text_color="white"
        )
        self.time_label.pack(pady=20)

        # --------- Bouton Retour ---------
        self.button_back = ctk.CTkButton(
            self.canvas,
            text="Retour au Menu Principal",
            command=self.return_to_menu,
            width=200,
            height=40,
            border_width=3,
            border_color="#191919",
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            corner_radius=10,
            text_color="white",
            font=("Orbitron", 16)
        )
        self.button_back.place(relx=0.9, rely=0.95, anchor="center")
        self.widgets.append(self.button_back)

        print("Interface Kartrack LIVE affichée !")

    def return_to_menu(self):
        for widget in self.widgets:
            widget.destroy()
        self.show_main_menu()
