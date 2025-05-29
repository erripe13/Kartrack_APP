import customtkinter as ctk
from PIL import Image, ImageTk, ImageFont
from PIL.Image import Resampling
# from karttrack_app import KartTrackApp
from race_interface import RaceInterface
from form_interface import FormulaireInterface
# from review_interface import ReviewInterface
import pywinstyles as pywin


PORT = "COM4"
BAUDRATE = 115200

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("KartTrack Interface")
        ctk.FontManager.load_font("fonts/Orbitron_Black.ttf")

        # Passer en mode plein écran
        self.root.attributes("-fullscreen", True)

        # Charger l'image de fond
        self.background_image = Image.open("images/background_2.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Créer un canvas pour l'image de fond
        self.canvas = ctk.CTkCanvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Charger la police personnalisée
        self.custom_font = ctk.CTkFont(family="Orbitron",size=20)

        # Ajouter les boutons directement sur le canvas
        self.title_label = ctk.CTkLabel(
            self.canvas,
            text="KartTrack",
            font=("Orbitron", 80,"bold"),
            bg_color="black"
        )
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        pywin.set_opacity(self.title_label, color="black")

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
        pywin.set_opacity(self.button1, color="black")

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
        pywin.set_opacity(self.button2, color="black")


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
        pywin.set_opacity(self.button3, color="black")

        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        resized_image = self.background_image.resize((new_width, new_height), Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.bg_item, image=self.background_photo)

    def race_interface(self):
        for widget in self.canvas.winfo_children():
            widget.place_forget()

        self.race_interface = RaceInterface(self.canvas, self.show_main_menu)

    def show_main_menu(self):
        self.canvas.delete("all")
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Replacer les boutons
        self.button1.place(relx=0.35, rely=0.5, anchor="center")
        self.button2.place(relx=0.50, rely=0.5, anchor="center")
        self.button3.place(relx=0.65, rely=0.5, anchor="center")

    def formulaire_interface(self):
        for widget in self.canvas.winfo_children():
            widget.place_forget()
        self.formulaire = FormulaireInterface(self.canvas, self.show_main_menu)


if __name__ == "__main__":

    root = ctk.CTk()
    app = MainInterface(root)
    root.mainloop()