import customtkinter as ctk
from PIL import Image, ImageTk, ImageFont
from PIL.Image import Resampling

class KartTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KartTrack Interface")

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
        try:
            self.custom_font = ImageFont.truetype("fonts/Orbitron_Black.ttf", 16)
        except Exception as e:
            print(f"Erreur lors du chargement de la police : {e}")
            self.custom_font = ("Arial", 16)  # Police de secours

        # Ajouter les boutons directement sur le canvas
        self.button1 = ctk.CTkButton(
            self.canvas,
            text="Kartrack LIVE",
            command=self.start_race,
            fg_color="blue",
            corner_radius=0,
            text_color="white",
            font=(self.custom_font, 16)
        )
        self.button1.place(relx=0.35, rely=0.5, anchor="center")

        self.button2 = ctk.CTkButton(
            self.canvas,
            text="Review",
            command=self.open_options,
            fg_color="blue",
            corner_radius=0,
            text_color="white",
            font=(self.custom_font, 16)
        )
        self.button2.place(relx=0.45, rely=0.5, anchor="center")

        self.button3 = ctk.CTkButton(
            self.canvas,
            text="Setup",
            command=self.root.quit,
            fg_color="blue",
            corner_radius=0,
            text_color="white",
            font=(self.custom_font, 16)
        )
        self.button3.place(relx=0.55, rely=0.5, anchor="center")

        self.button4 = ctk.CTkButton(
            self.canvas,
            text="Quitter",
            command=self.root.quit,
            fg_color="blue",
            corner_radius=0,
            text_color="white",
            font=(self.custom_font, 16)
        )
        self.button4.place(relx=0.65, rely=0.5, anchor="center")

        # Redimensionner l'image de fond lors du redimensionnement de la fenêtre
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        resized_image = self.background_image.resize((new_width, new_height), Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.bg_item, image=self.background_photo)

    def start_race(self):
        print("Course commencée !")

    def open_options(self):
        print("Options ouvertes !")

# Lancement de l'application
if __name__ == "__main__":
    root = ctk.CTk()
    app = KartTrackApp(root)
    root.mainloop()
