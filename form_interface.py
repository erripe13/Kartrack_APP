import customtkinter as ctk
import os
import pywinstyles as pywin


class FormulaireInterface:
    def __init__(self, canvas, show_main_menu):
        self.canvas = canvas
        self.show_main_menu = show_main_menu
        self.widgets = []

        # Cadre principal qui contient tout le formulaire
        self.entry_frame = ctk.CTkFrame(
            self.canvas,
            width=900,
            height=600,
            corner_radius=10,
            bg_color="black",
            fg_color="#222222"
        )
        pywin.set_opacity(self.entry_frame, color="black")
        pywin.set_opacity(self.entry_frame, color="#222222")
        self.entry_frame.place(relx=0.5, rely=0.5, anchor="center")


        self.widgets.append(self.entry_frame)

        # Encadré pour le "Nom de course" (au-dessus des sections)
        self.add_course_name_block()

        # Création des trois sections côte à côte
        self.create_sections()

        # Boutons Enregistrer et Retour
        self.save_button = ctk.CTkButton(
            self.entry_frame,
            text="Enregistrer",
            command=self.save_to_txt,
            font=("Orbitron", 16),
            fg_color="#DB3E39",
            bg_color="black",
            text_color="white"
        )
        self.save_button.grid(row=3, column=1, padx=10, pady=10)

        self.back_button = ctk.CTkButton(
            self.entry_frame,
            text="Retour",
            command=self.return_to_menu,
            font=("Orbitron", 16),
            fg_color="#DB3E39",
            bg_color="black",
            text_color="white"
        )
        self.back_button.grid(row=4, column=1, padx=10, pady=(0, 10))

    def add_course_name_block(self):
        """
        Ajoute un encadré au-dessus des sections pour saisir le Nom de course.
        """
        course_frame = ctk.CTkFrame(
            self.entry_frame,
            fg_color="#333333",
            bg_color="black",
            corner_radius=10
        )
        course_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        course_label = ctk.CTkLabel(
            course_frame,
            text="Nom de course",
            font=("Orbitron", 16),
            text_color="#DB3E39"
        )
        course_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        course_entry = ctk.CTkEntry(
            course_frame,
            placeholder_text="Entrez le nom de la course...",
            font=("Orbitron", 16),
            fg_color="white",
            bg_color="black",
            text_color="black"
        )
        course_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

    def create_sections(self):
        """
        Crée trois sections horizontalement alignées en dessous du Nom de course
        """
        section_titles = ["Début", "Section 1", "Section 2"]

        for col, section_title in enumerate(section_titles):
            section_frame = ctk.CTkFrame(self.entry_frame, corner_radius=10, fg_color="#333333")
            section_frame.grid(row=1, column=col, padx=10, pady=10)

            title_label = ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=("Orbitron", 16),
                text_color="#DB3E39"
            )
            title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

            self.add_section_fields(section_frame)

    def add_section_fields(self, frame):
        """
        Ajoute deux champs (Longitude et Latitude) dans une section :
        - Ligne 1 : Longitude
        - Ligne 2 : Latitude
        """
        row_title_longitude = ctk.CTkLabel(
            frame,
            text="Longitude :",
            anchor="w",
            font=("Orbitron", 16),
            text_color="#DB3E39"
        )
        row_title_longitude.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_longitude = ctk.CTkEntry(
            frame,
            placeholder_text="Longitude",
            font=("Orbitron", 16)
        )
        entry_longitude.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        row_title_latitude = ctk.CTkLabel(
            frame,
            text="Latitude :",
            anchor="w",
            font=("Orbitron", 16),
            text_color="#DB3E39"
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
        Après une sauvegarde réussie, la page se ferme automatiquement
        et retourne à la page précédente après 5 secondes.
        """
        # Définir le chemin du dossier
        directory = "Data_course"

        # Créer le dossier s'il n'existe pas
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Récupérer les données des champs
        course_name = self.entry_frame.winfo_children()[0].winfo_children()[1].get()  # Champ Nom de course
        data = []

        for section_frame in self.entry_frame.winfo_children()[1:4]:
            # Filtrer les entrées uniquement de type CTkEntry
            entries = [child for child in section_frame.winfo_children() if isinstance(child, ctk.CTkEntry)]

            if len(entries) == 2:
                longitude = entries[0].get().strip()
                latitude = entries[1].get().strip()
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

        print(f"Données sauvegardées dans : {directory}.")

        # Afficher une confirmation dans l'interface utilisateur
        success_label = ctk.CTkLabel(
            self.entry_frame,
            text=f"Données sauvegardées dans le dossier '{directory}'.",
            font=("Orbitron", 16),
            text_color="green",
        )
        success_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Planifier la fermeture de la page après 5 secondes
        self.entry_frame.after(5000, self.close_form_interface)

    def close_form_interface(self):
        """
        Ferme la fenêtre actuelle et retourne au menu principal.
        """
        # Détruire tous les widgets pour fermer la page
        for widget in self.widgets:
            widget.destroy()

        # Appeler la méthode pour retourner au menu précédent
        self.show_main_menu()

    def return_to_menu(self):
        """
        Retourne directement au menu principal.
        """
        for widget in self.widgets:
            widget.destroy()
        self.show_main_menu()
