import customtkinter as ctk
import os



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
            bg_color="black",# Coins arrondis
            fg_color="#222222"  # Fond gris foncé pour le formulaire
        )
        self.entry_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.widgets.append(self.entry_frame)

        # Encadré pour le "Nom de course" (au-dessus des sections)
        self.add_course_name_block()  # Appelle la méthode pour ajouter le bloc Nom de course

        # Création des trois sections côte à côte
        self.create_sections()

        # Boutons Enregistrer et Retour (placés sous la Section 2, au centre de l'interface)
        self.save_button = ctk.CTkButton(
            self.entry_frame,
            text="Enregistrer en .txt",
            command=self.save_to_txt,
            font=("Orbitron", 16),
            fg_color="#DB3E39",  # Couleur rouge
            text_color="white"  # Texte blanc
        )
        self.save_button.grid(row=3, column=1, padx=10, pady=10)  # Aligné sous Section 2

        self.back_button = ctk.CTkButton(
            self.entry_frame,
            text="Retour",
            command=self.return_to_menu,
            font=("Orbitron", 16),
            fg_color="#DB3E39",  # Couleur rouge
            text_color="white"  # Texte blanc
        )
        self.back_button.grid(row=4, column=1, padx=10, pady=(0, 10))  # Placé juste en dessous du bouton Enregistrer

    def add_course_name_block(self):
        """
        Ajoute un encadré au-dessus des sections pour saisir le Nom de course.
        """
        course_frame = ctk.CTkFrame(
            self.entry_frame,
            fg_color="#333333",  # Couleur de fond pour l'encadré
            corner_radius=10  # Coins légèrement arrondis
        )
        course_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Label pour "Nom de course"
        course_label = ctk.CTkLabel(
            course_frame,
            text="Nom de course",
            font=("Orbitron", 16),
            text_color="#DB3E39"  # Texte rouge
        )
        course_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        # Champ d'entrée pour le Nom de course
        course_entry = ctk.CTkEntry(
            course_frame,
            placeholder_text="Entrez le nom de la course...",
            font=("Orbitron", 16),
            fg_color="white",  # Champ de texte blanc
            text_color="black"  # Texte noir
        )
        course_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

    def create_sections(self):
        """
        Crée trois sections horizontalement alignées en dessous du Nom de course
        """
        section_titles = ["Début", "Section 1", "Section 2"]  # Titres pour chaque section

        # Création des trois sections alignées horizontalement
        for col, section_title in enumerate(section_titles):
            # Sous-cadre pour chaque section
            section_frame = ctk.CTkFrame(self.entry_frame, corner_radius=10, fg_color="#333333")
            section_frame.grid(row=1, column=col, padx=10, pady=10)

            # Ajouter le titre de la section
            title_label = ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=("Orbitron", 16),
                text_color="#DB3E39"  # Texte rouge
            )
            title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

            # Ajouter champs pour chaque ligne de la section
            self.add_section_fields(section_frame)

    def add_section_fields(self, frame):
        """
        Ajoute deux champs (Longitude et Latitude) dans une section :
        - Ligne 1 : Longitude
        - Ligne 2 : Latitude
        """
        # Ligne pour Longitude
        row_title_longitude = ctk.CTkLabel(
            frame,
            text="Longitude :",
            anchor="w",
            font=("Orbitron", 16),
            text_color="#DB3E39"  # Rouge pour le label
        )
        row_title_longitude.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_longitude = ctk.CTkEntry(
            frame,
            placeholder_text="Longitude",
            font=("Orbitron", 16)
        )
        entry_longitude.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Ligne pour Latitude
        row_title_latitude = ctk.CTkLabel(
            frame,
            text="Latitude :",
            anchor="w",
            font=("Orbitron", 16),
            text_color="#DB3E39"  # Rouge pour le label
        )
        row_title_latitude.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        entry_latitude = ctk.CTkEntry(
            frame,
            placeholder_text="Latitude",
            font=("Orbitron", 16)
        )
        entry_latitude.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def save_to_txt(self):
        """
            Enregistre les données du formulaire dans un fichier .txt dans le dossier Data_course.
            Si le dossier n'existe pas, il est créé.
            """
        # Définir le chemin du dossier
        directory = "Data_course"

        # Créer le dossier s'il n'existe pas
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Récupérer les données des champs
        course_name = self.entry_frame.winfo_children()[0].winfo_children()[1].get()  # Champ Nom de course
        data = []

        for section_frame in self.entry_frame.winfo_children()[1:4]:  # Sections Début, Section 1, Section 2
            # Filtrer les entrées uniquement de type CTkEntry
            entries = [child for child in section_frame.winfo_children() if isinstance(child, ctk.CTkEntry)]

            # S'assurer qu'il y a bien 2 entrées (longitude et latitude)
            if len(entries) == 2:
                longitude = entries[0].get().strip()  # Lecture de l'entrée "Longitude"
                latitude = entries[1].get().strip()  # Lecture de l'entrée "Latitude"
                data.append((longitude, latitude))
            else:
                print("Erreur : impossible de trouver les champs Longitude et Latitude dans l'une des sections.")

        # Construire le nom du fichier
        file_name = f"{course_name if course_name.strip() else 'Course_sans_nom'}.txt"
        file_path = os.path.join(directory, file_name)

        # Écrire les données dans le fichier
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Nom de la course : {course_name}\n\n")

            for i, values in enumerate(data, start=1):
                file.write(f"Section {i}:\n")
                file.write(f"  Longitude : {values[0]}\n")
                file.write(f"  Latitude : {values[1]}\n")
                file.write("\n")

        print(f"Données sauvegardées dans : {file_path}.")

        print(f"Données sauvegardées dans : {file_path}.")

    def return_to_menu(self):
        """Retourne au menu principal"""
        for widget in self.widgets:
            widget.destroy()
        self.show_main_menu()
