import customtkinter as ctk
from PIL import Image, ImageTk, ImageFont
from PIL.Image import Resampling
# from karttrack_app import KartTrackApp
from race_interface import RaceInterface
from form_interface import FormulaireInterface
# from review_interface import ReviewInterface


PORT = "COM3"
BAUDRATE = 9600

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("KartTrack Interface")
        ctk.FontManager.load_font("fonts/Orbitron_Black.ttf")

        # Passer en mode plein écran
        self.root.attributes("-fullscreen", True)

        # Charger l'image de fond
        self.background_image = Image.open("images/background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Créer un canvas pour l'image de fond
        self.canvas = ctk.CTkCanvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Charger la police personnalisée
        self.custom_font = ctk.CTkFont(family="Orbitron",size=20)

        # Ajouter les boutons directement sur le canvas
        self.button1 = ctk.CTkButton(
            self.canvas,
            text="Kartrack LIVE",
            command=self.race_interface,
            width=200,
            height=100,
            border_width=3,
            border_color="#191919",
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            corner_radius=10,
            text_color="white",
            font=("Orbitron",20)
        )
        self.button1.place(relx=0.35, rely=0.5, anchor="center")

        self.button2 = ctk.CTkButton(
            self.canvas,
            text="Formulaire Circuit",
            command=self.formulaire_interface,
            width=200,
            height=100,
            border_width=3,
            border_color="#191919",
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            corner_radius=10,
            text_color="white",
            font=("Orbitron", 20)
        )
        self.button2.place(relx=0.50, rely=0.5, anchor="center")

        self.button3 = ctk.CTkButton(
            self.canvas,
            text="Quitter",
            command=self.root.quit,
            width=200,
            height=100,
            border_width=3,
            border_color="#191919",
            fg_color=("#DB3E39", "#821D1A"),
            bg_color="black",
            corner_radius=10,
            text_color="white",
            font=("Orbitron", 20)
        )
        self.button3.place(relx=0.65, rely=0.5, anchor="center")


        # Redimensionner l'image de fond lors du redimensionnement de la fenêtre
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        resized_image = self.background_image.resize((new_width, new_height), Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.bg_item, image=self.background_photo)

    def race_interface(self):
        # Masquer l'interface principale
        for widget in self.canvas.winfo_children():
            widget.place_forget()

        # Afficher l'interface de la course
        self.race_interface = RaceInterface(self.canvas, self.show_main_menu)
        # suppose que tu as accès à l'instance ici

    def show_main_menu(self):
        # Remettre le fond principal
        self.canvas.delete("all")  # Supprime tous les éléments (dont le fond course)
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Replacer les boutons
        self.button1.place(relx=0.35, rely=0.5, anchor="center")
        self.button2.place(relx=0.50, rely=0.5, anchor="center")
        self.button3.place(relx=0.65, rely=0.5, anchor="center")

    def formulaire_interface(self):
        for widget in self.canvas.winfo_children():
            widget.place_forget()
        self.formulaire = FormulaireInterface(self.canvas, self.show_main_menu)


# Lancement de l'application
if __name__ == "__main__":

    root = ctk.CTk()
    app = MainInterface(root)
    root.mainloop()