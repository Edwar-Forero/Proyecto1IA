import tkinter as tk
from tkinter import messagebox
from gui.editor_mapa import EditorMapa
""" from utils.helpers import centrar_ventana """


class VentanaInicio(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Proyecto IA - La Hormiga y el Hongo Mágico 🐜🍄")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        """ ancho, alto = 400, 300
        centrar_ventana(self, ancho, alto) """

        # --- Título principal ---
        titulo = tk.Label(
            self,
            text="Configuración del entorno",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        titulo.pack(pady=20)

        # --- Entrada de filas ---
        frame_filas = tk.Frame(self, bg="#f0f0f0")
        frame_filas.pack(pady=10)
        tk.Label(frame_filas, text="Número de filas:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.entry_filas = tk.Entry(frame_filas, width=10, justify="center")
        self.entry_filas.pack(side=tk.LEFT)

        # --- Entrada de columnas ---
        frame_columnas = tk.Frame(self, bg="#f0f0f0")
        frame_columnas.pack(pady=10)
        tk.Label(frame_columnas, text="Número de columnas:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.entry_columnas = tk.Entry(frame_columnas, width=10, justify="center")
        self.entry_columnas.pack(side=tk.LEFT)

        # --- Botón para crear la matriz ---
        boton_crear = tk.Button(
            self,
            text="Crear matriz",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.crear_matriz
        )
        boton_crear.pack(pady=20)

    def crear_matriz(self):
        """Lee los valores de filas y columnas y abre la ventana de edición del mapa"""
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())

            if filas <= 0 or columnas <= 0:
                raise ValueError

            # Cierra esta ventana y abre el editor del mapa
            self.destroy()
            editor = EditorMapa(filas, columnas)
            editor.mainloop()

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números enteros positivos.")


