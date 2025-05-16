import threading
import serial
import time

class LoRaReader(threading.Thread):
    def __init__(self, port, baudrate, callback):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.callback = callback  # Fonction qui reçoit latitude, longitude
        self.running = True

    def run(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=2) as ser:
                while self.running:
                    line = ser.readline().decode("utf-8").strip()
                    if line:
                        try:
                            lat, lon = map(float, line.split(","))
                            self.callback(lat, lon)  # Envoie à RaceInterface
                        except Exception:
                            pass
        except Exception as e:
            print("Erreur LoRa:", e)