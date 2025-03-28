# race_interface.py
import customtkinter as ctk
class RaceInterface:
    def __init__(self, canvas, show_main_menu):
        self.canvas = canvas
        self.show_main_menu = show_main_menu
        self.widgets = []

        # Créer un bouton pour revenir au menu principal
        self.button_back = ctk.CTkButton(
            self.canvas,
            text="Retour au Menu Principal",
            command=self.return_to_menu,
            width=200,
            height=100,
            border_width=3,
            border_color="#191919",
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            corner_radius=10,
            text_color="white",
            font=("Orbitron", 16)
        )
        self.button_back.place(relx=0.5, rely=0.5, anchor="center")
        self.widgets.append(self.button_back)

        print("Interface Kartrack LIVE affichée !")

    def return_to_menu(self):
        for widget in self.widgets:
            widget.destroy()
        self.show_main_menu()
