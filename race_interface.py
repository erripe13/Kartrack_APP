import time
import customtkinter as ctk
import pywinstyles as pywin
import tkintermapview
from PIL import ImageTk, Image
import weather_mod as wm
import threading
from LoRa_car import LoRaReader


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

        self.map_frame = None
        self.time_frame = None
        self.banner = None

        self.splits = []

        try:
            self.vehicle_image = Image.open("images/vehicle.jpg")
            self.vehicle_image = self.vehicle_image.resize((30, 30))  # Redimensionner l'image
            self.vehicle_icon = ImageTk.PhotoImage(self.vehicle_image)
            self.vehicle_marker = None
        except Exception as e:
            print(f"Erreur lors du chargement de l'image du véhicule : {e}")
            self.vehicle_icon = None

            # Initialiser le thread LoRa avec le callback
        self.lora_thread = LoRaReader(
            on_position_callback=self.update_car_position
        )
        self.lora_thread.start()

        pywin.set_opacity(self.entry_frame, color="#191919")


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
            font=("Orbitron", 40),
            corner_radius=0,
            text_color="white"
        )
        self.track_name_label.place(relx=0.1, rely=0.5, anchor="center")
        self.widgets.append(self.track_name_label)

        pywin.set_opacity(self.banner, color="#333333",value=0.9)


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

        pywin.set_opacity(self.map_frame, color="#222222")


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
        pywin.set_opacity(self.time_frame, color="#1A1D21")


        self.time_label = ctk.CTkLabel(
            self.time_frame,
            text="Temps",
            font=("Orbitron", 40),
            corner_radius=0,
            text_color="white"
        )
        self.time_label.place(relx=0.5, rely=0.1, anchor="center")

        self.chrono_label = ctk.CTkLabel(
            self.time_frame,
            text="00:00:00",
            font=("Orbitron", 30, "bold"),
            text_color="white")

        self.chrono_label.place(relx=0.5, rely=0.4, anchor="center")
        self.start_time = time.time()

        self.start_button = ctk.CTkButton(
            self.time_frame,
            text="Démarrer",
            command=self.toggle_chrono,  # Changer la commande
            fg_color=("#DB3E39", "#821D1A"),
            width=100,
            height=40,
            font=("Orbitron", 16)
        )
        self.start_button.place(relx=0.3, rely=0.3, anchor="center")

        self.reset_button = ctk.CTkButton(
            self.time_frame,
            text="Réinitialiser",
            command=self.reset_chrono,
            fg_color=("#DB3E39", "#821D1A"),
            width=100,
            height=40,
            font=("Orbitron", 16)
        )
        self.reset_button.place(relx=0.7, rely=0.3, anchor="center")

        self.test_button = ctk.CTkButton(
            self.time_frame,
            text="Test Déplacement",
            command=self.start_test_movement,
            fg_color=("#DB3E39", "#821D1A"),
            width=100,
            height=40,
            font=("Orbitron", 16)
        )
        self.test_button.place(relx=0.5, rely=0.85, anchor="center")

        self.test_running = False
        self.test_thread = None

        self.start_time = None
        self.running = False
        self.elapsed_time = 0

        self.update_chrono()

        self.widgets.append(self.chrono_label)
        self.widgets.append(self.time_label)
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

        # --- Boutons S1, S2, S3 ---
        self.s1_button = ctk.CTkButton(
            self.time_frame,
            text="S1",
            fg_color=("#DB3E39", "#821D1A"),
            width=80,
            height=40,
            font=("Orbitron", 16),
            command=lambda: self.record_split(1),
        )
        self.s1_button.place(relx=0.25, rely=0.55, anchor="center")

        self.s2_button = ctk.CTkButton(
            self.time_frame,
            text="S2",
            fg_color=("#DB3E39", "#821D1A"),
            width=80,
            height=40,
            font=("Orbitron", 16),
            command=lambda: self.record_split(2)
        )
        self.s2_button.place(relx=0.5, rely=0.55, anchor="center")

        self.s3_button = ctk.CTkButton(
            self.time_frame,
            text="S3",
            fg_color=("#DB3E39", "#821D1A"),
            width=80,
            height=40,
            font=("Orbitron", 16),
            command=lambda: self.record_split(3)
        )
        self.s3_button.place(relx=0.75, rely=0.55, anchor="center")

        # Affichage des temps de splits
        self.split_labels = [
            ctk.CTkLabel(self.time_frame, text="S1 : --:--:--", font=("Orbitron", 16), text_color="white"),
            ctk.CTkLabel(self.time_frame, text="S2 : --:--:--", font=("Orbitron", 16), text_color="white"),
            ctk.CTkLabel(self.time_frame, text="S3 : --:--:--", font=("Orbitron", 16), text_color="white"),
        ]
        for i, label in enumerate(self.split_labels):
            label.place(relx=0.5, rely=0.65 + i * 0.06, anchor="center")

        self.start_time = None
        self.running = False
        self.elapsed_time = 0

        self.update_chrono()

        self.widgets.append(self.chrono_label)
        self.widgets.append(self.time_label)
        self.widgets.append(self.time_frame)
        self.widgets += [self.s1_button, self.s2_button, self.s3_button] + self.split_labels

    def search_event(self, event=None):
        """Méthode appelée depuis l'UI, lance la recherche dans un thread séparé."""
        thread = threading.Thread(target=self._search_event_worker, args=(event,), daemon=True)
        thread.start()

    def _search_event_worker(self, event):
        """Travail réel de recherche, s'exécute en tâche de fond."""
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

        # On appelle la mise à jour de la map dans le thread principal via after
        self.canvas.after(0, lambda: self.map_widget.set_position(latitude, longitude, zoom=10))


    def start_chrono(self):
        if not self.running:
            self.start_time = time.perf_counter()
            self.running = True
            self.update_chrono()

    def toggle_chrono(self):
        if not self.running:
            if self.start_time is None:
                self.start_time = time.perf_counter()
                self.elapsed_time = 0
            else:
                self.start_time = time.perf_counter() - self.elapsed_time
            self.running = True
            self.start_button.configure(text="Pause")
            self.update_chrono()
        else:
            self.running = False
            self.elapsed_time = time.perf_counter() - self.start_time
            self.start_button.configure(text="Reprendre")

    def update_chrono(self):
        if self.running:
            elapsed_time = time.perf_counter() - self.start_time
            minutes, remainder = divmod(int(elapsed_time), 60)
            seconds = int(remainder)
            hundredths = int((elapsed_time - int(elapsed_time)) * 100)
            time_string = f"{minutes:02}:{seconds:02}:{hundredths:02}"
            self.chrono_label.configure(text=time_string)
            self.chrono_label.after(50, self.update_chrono)

    def stop_chrono(self):
        self.running = False

    def record_split(self, split_number):
        """Enregistre le temps courant du chrono lors de l'appui sur S1 / S2 / S3."""
        if self.running and self.start_time is not None:
            current_time = time.perf_counter() - self.start_time
            minutes, remainder = divmod(int(current_time), 60)
            seconds = int(remainder)
            hundredths = int((current_time - int(current_time)) * 100)
            time_string = f"{minutes:02}:{seconds:02}:{hundredths:02}"
            self.splits = self.splits[:split_number-1] + [time_string]
            while len(self.splits) < 3:
                self.splits.append("--:--:--")
            self.split_labels[split_number-1].configure(text=f"S{split_number} : {time_string}")


    def reset_chrono(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.chrono_label.configure(text="00:00:00")
        self.start_button.configure(text="Démarrer")
        self.splits = []
        for i, label in enumerate(self.split_labels):
            label.configure(text=f"S{i + 1} : --:--:--")

    def return_to_menu(self):
        for widget in self.widgets:
            widget.destroy()
        self.entry_frame.destroy()
        self.show_main_menu()

    def update_car_position(self, latitude, longitude):
        self.canvas.after(0, lambda: self._update_vehicle_marker(latitude, longitude))

    def _update_vehicle_marker(self, latitude, longitude):
        try:
            if self.vehicle_marker is None:
                self.vehicle_marker = self.map_widget.set_marker(
                    latitude,
                    longitude,
                    icon=self.vehicle_icon
                )
            else:
                self.vehicle_marker.set_position(latitude, longitude)


        except Exception as e:
            print(f"Erreur lors de la mise à jour du marqueur : {e}")

    def start_test_movement(self):

        if not self.test_running:
            self.test_running = True
            self.test_button.configure(text="Arrêter Test")
            # Créer et démarrer le thread de test
            self.test_thread = threading.Thread(target=self.test_position)
            self.test_thread.daemon = True
            self.test_thread.start()
        else:
            self.test_running = False
            self.test_button.configure(text="Test Déplacement")

    def test_position(self):
        test_coords = [
            (49.0388, 2.0784),
            (49.0390, 2.0790),
            (49.0395, 2.0795),
            (49.0400, 2.0800),
            (49.0405, 2.0795),
            (49.0400, 2.0790),
            (49.0395, 2.0785),
            (49.0388, 2.0784)
        ]

        while self.test_running:
            for lat, lon in test_coords:
                if not self.test_running:
                    break
                self.update_car_position(lat, lon)
                time.sleep(0.5)
