import tkinter as tk
from utils.helpers import centrar_ventana

class Simulador(tk.Tk):
    def __init__(self, entorno):
        super().__init__()
        self.title("Simulador - Hormiga en acción 🐜")
        self.geometry("400x400")
        label = tk.Label(self, text="Aquí irá la simulación del algoritmo", font=("Arial", 14))
        label.pack(expand=True)

        ancho, alto = 400, 300
        centrar_ventana(self, ancho, alto)
