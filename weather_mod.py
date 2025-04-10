import customtkinter as ctk
import os
from dotenv import load_dotenv
import requests
from tkinter import Label,Tk,PhotoImage
from dico_meteo import GIF_FOLDER, CONDITIONS_TO_GIFS
from PIL import Image, ImageTk, ImageFont

dotenv_path = ".venv/.env"
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("WEATHER_API_KEY")
URL_CURRENT = "http://api.weatherapi.com/v1/current.json"
URL_FORECAST = "http://api.weatherapi.com/v1/forecast.json"


def get_current_weather_conditions(self):
    # Coordonnées par défaut pour Cergy
    default_lat = 49.0388
    default_long = 2.0784

    # Récupérer les valeurs saisies par l'utilisateur
    latitude_input = self.entry_lat.get().strip()
    longitude_input = self.entry_long.get().strip()

    # Si les champs sont vides, utiliser les coordonnées par défaut
    if not latitude_input or not longitude_input:
        latitude = default_lat
        longitude = default_long
    else:
        try:
            latitude = float(latitude_input)
            longitude = float(longitude_input)
        except ValueError:
            latitude = default_lat
            longitude = default_long

    # Préparer les paramètres pour l'API avec les coordonnées finales
    params = {
        "key": API_KEY,
        "q": f"{latitude},{longitude}",  # Format {lat,long}
        "lang": "fr"  # Langue française
    }

    print(f"Coordonnées envoyées : lat={latitude}, long={longitude}")  # Debugging

    # Effectuer la requête vers l'API
    response = requests.get(URL_CURRENT, params=params)

    if response.status_code == 200:
        # Parse les données si la requête est un succès
        data = response.json()
        temperature = data["current"]["temp_c"]
        condition_text = data["current"]["condition"]["text"]

        # Obtenir l'icône GIF associé
        gif_path = get_weather_gif(condition_text)

        return {
            "température": temperature,
            "condition_text": condition_text,
            "gif_path": gif_path  # Inclure le chemin du fichier GIF météo
        }
    else:
        # En cas d'échec de la requête
        print(f"Erreur API : code {response.status_code}, détail : {response.text}")
        return {"erreur": "Impossible de récupérer les données météo."}


def display_weather(self):
    default_lat = 49.0388
    default_long = 2.0784

    # Récupérer les valeurs saisies par l'utilisateur
    latitude_input = self.entry_lat.get().strip()
    longitude_input = self.entry_long.get().strip()
    weather_data = get_current_weather_conditions(self)

    if "erreur" in weather_data:
        print("Erreur : ", weather_data["erreur"])
        return

        # Supprimer tout widget existant dans le bandeau avant d'afficher la météo
    for widget in self.banner.winfo_children():
        widget.destroy()

        # Extraire les données météo
    température = weather_data.get('température', 'N/A')
    condition = weather_data.get('condition_text', 'N/A')
    gif_path = weather_data.get('gif_path', '')

        # Charger l'icône météo (au centre)
    try:
        icon_image = Image.open(gif_path)
        icon_photo = ImageTk.PhotoImage(icon_image)

            # Créer un label pour afficher l'icône météo
        icon_label = Label(self.banner, image=icon_photo,bg="#333333")
        icon_label.image = icon_photo  # Sauvegarder la référence pour éviter la suppression
        icon_label.pack(side="top", pady=10)
    except:
        print(f"Erreur lors du chargement de l'icône météo : {gif_path}")

        # Ajouter la température et les conditions météo (centré)
    weather_label = ctk.CTkLabel(
        self.banner,
        text=f"{température}°C | {condition}",
        font=("Orbitron", 20, "bold"),
        text_color="#821D1A",
        bg_color="#333333"
        )
    weather_label.pack(side="top")


def get_weather_gif(condition_text):
    return GIF_FOLDER + CONDITIONS_TO_GIFS.get(condition_text, "icons8-partly-cloudy.gif")