import customtkinter as ctk


class FormulaireInterface:
    def __init__(self, canvas, show_main_menu):
        self.canvas = canvas
        self.show_main_menu = show_main_menu
        self.widgets = []

        # Cadre principal qui contient tout le formulaire
        self.entry_frame = ctk.CTkFrame(
            self.canvas,
            width=900,  # Largeur ajustée pour trois sections
            height=600,
            corner_radius=10,
            fg_color="#222222"
        )
        self.entry_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.widgets.append(self.entry_frame)

        # Création des trois sections côte à côte
        self.create_sections()

        # Boutons Enregistrer et Retour
        self.save_button = ctk.CTkButton(self.entry_frame, text="Enregistrer en .txt", command=self.save_to_txt, font=("Orbitron", 16))
        self.save_button.grid(row=1, column=1, columnspan=3, pady=20)

        self.back_button = ctk.CTkButton(self.entry_frame, text="Retour", command=self.return_to_menu, font=("Orbitron", 16))
        self.back_button.grid(row=2, column=1, columnspan=3, pady=(0, 10))

    def create_sections(self):
        """
        Crée trois sections horizontalement alignées.
        Chaque section aide à structurer les titres et les champs
        """
        section_titles = ["Section 1", "Section 2", "Section 3"]  # Titres pour chaque section

        # Création des trois sections alignées horizontalement
        for col, section_title in enumerate(section_titles):
            # Sous-cadre pour chaque section
            section_frame = ctk.CTkFrame(self.entry_frame, corner_radius=10, fg_color="#333333")
            section_frame.grid(row=0, column=col, padx=10, pady=10)

            # Ajouter le titre de la section
            title_label = ctk.CTkLabel(section_frame, text=section_title, font=("Orbitron", 16))
            title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

            # Ajouter champs pour chaque ligne de la section
            self.add_section_fields(section_frame)

    def add_section_fields(self, frame):
        """
        Ajoute deux lignes de champs dans une section:
        - Ligne 1 : Titre + Longitude + Latitude
        - Ligne 2 : Titre différent + Longitude + Latitude
        """
        # Ligne 1
        row_title_1 = ctk.CTkLabel(frame, text="Titre Ligne 1 :", anchor="w", font=("Orbitron", 16))
        row_title_1.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_longitude_1 = ctk.CTkEntry(frame, placeholder_text="Longitude", font=("Orbitron", 16))
        entry_longitude_1.grid(row=1, column=1, padx=5, pady=5)

        entry_latitude_1 = ctk.CTkEntry(frame, placeholder_text="Latitude", font=("Orbitron", 16))
        entry_latitude_1.grid(row=1, column=2, padx=5, pady=5)

        # Ligne 2
        row_title_2 = ctk.CTkLabel(frame, text="Titre Ligne 2 :", anchor="w", font=("Orbitron", 16))
        row_title_2.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        entry_longitude_2 = ctk.CTkEntry(frame, placeholder_text="Longitude", font=("Orbitron", 16))
        entry_longitude_2.grid(row=2, column=1, padx=5, pady=5)

        entry_latitude_2 = ctk.CTkEntry(frame, placeholder_text="Latitude", font=("Orbitron", 16))
        entry_latitude_2.grid(row=2, column=2, padx=5, pady=5)

    def save_to_txt(self):
        """
        Enregistre les données du formulaire dans un fichier .txt
        (à adapter en fonction des champs réels à traiter)
        """
        # Exemple simple d'enregistrement (peut varier selon les données de vos champs)
        print("Données sauvegardées (implémentation à ajouter).")

    def return_to_menu(self):
        """Retourne au menu principal"""
        for widget in self.widgets:
            widget.destroy()
        self.show_main_menu()
