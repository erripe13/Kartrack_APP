import threading
import serial

PORT = 'COM9'
BAUDRATE = 115200

class LoRaReader(threading.Thread):
    def __init__(self,on_position_callback):
        super().__init__(daemon=True)
        self.on_position_callback = on_position_callback
        self.running = True

    def run(self):
        try:
            with serial.Serial(stimeout=2) as ser:
                while self.running:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        try:
                            lat, lon = map(float, line.split(","))
                            self.on_position_callback(lat, lon)
                        except Exception:
                            pass
        except Exception as e:
            print("Erreur série LoRa:", e)
