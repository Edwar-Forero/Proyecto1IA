import tkinter as tk
from tkinter import messagebox
from core.entorno import Entorno
from gui.simulador import Simulador


class EditorMapa(tk.Tk):
    def __init__(self, filas, columnas):
        super().__init__()

        self.title("Editor del Mapa 🐜🍄")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        self.filas = filas
        self.columnas = columnas
        self.celda_size = 40
        self.modo = tk.StringVar(value="hormiga")

        # --- Crear entorno ---
        self.entorno = Entorno(filas, columnas)

        # --- Canvas principal ---
        self.canvas = tk.Canvas(
            self,
            width=self.columnas * self.celda_size,
            height=self.filas * self.celda_size,
            bg="white"
        )
        self.canvas.pack(padx=10, pady=10)
        self.dibujar_cuadricula()
        self.canvas.bind("<Button-1>", self.colocar_elemento)

        # --- Controles laterales ---
        frame_controles = tk.Frame(self, bg="#f0f0f0")
        frame_controles.pack(pady=10)

        tk.Label(frame_controles, text="Modo de colocación:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(
            row=0, column=0, columnspan=4, pady=5
        )

        modos = [
            ("Hormiga 🐜", "hormiga"),
            ("Hongo 🍄", "meta"),
            ("Veneno ☠️", "veneno"),
            ("Borrar ❌", "borrar")
        ]
        for i, (texto, valor) in enumerate(modos):
            tk.Radiobutton(
                frame_controles,
                text=texto,
                variable=self.modo,
                value=valor,
                bg="#f0f0f0"
            ).grid(row=1, column=i, padx=5)

        # --- Botones de algoritmo ---
        frame_beam = tk.Frame(frame_controles, bg="#f0f0f0")
        frame_beam.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(
            frame_beam,
            text="Usar Beam Search 🔍",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            command=lambda: self.iniciar_busqueda("beam")
        ).pack(side=tk.LEFT, padx=(0, 5))

        tk.Label(frame_beam, text="β:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.entry_filas = tk.Entry(frame_beam, width=5, justify="center")
        self.entry_filas.pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(
            frame_controles,
            text="Usar Dynamic Weighted A* ⚖️",
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            command=lambda: self.iniciar_busqueda("dynamic")
        ).grid(row=3, column=2, columnspan=2, padx=10, pady=5)

    # -----------------------------
    # Dibuja la cuadrícula vacía
    # -----------------------------
    def dibujar_cuadricula(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                x1 = j * self.celda_size
                y1 = i * self.celda_size
                x2 = x1 + self.celda_size
                y2 = y1 + self.celda_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="white")

    # -----------------------------
    # Coloca o borra un elemento
    # -----------------------------
    def colocar_elemento(self, event):
        fila = event.y // self.celda_size
        col = event.x // self.celda_size

        modo = self.modo.get()
        if modo == "hormiga":
            self.entorno.colocar_hormiga((fila, col))
        elif modo == "meta":
            self.entorno.colocar_meta((fila, col))
        elif modo == "veneno":
            self.entorno.colocar_veneno((fila, col))
        elif modo == "borrar":
            self.entorno.borrar_elemento((fila, col))

        self.actualizar_canvas()

    # -----------------------------
    # Redibuja el mapa
    # -----------------------------
    def actualizar_canvas(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                x1 = j * self.celda_size
                y1 = i * self.celda_size
                x2 = x1 + self.celda_size
                y2 = y1 + self.celda_size

                celda = self.entorno.matriz[i][j]

                if celda == "H":  # Hormiga
                    color = "orange"
                elif celda == "M":  # Meta
                    color = "green"
                elif celda == "V":  # Veneno
                    color = "red"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=color)

    # -----------------------------
    # Abre la ventana de simulación
    # -----------------------------
    def iniciar_busqueda(self, algoritmo):
        if not self.entorno.pos_hormiga or not self.entorno.pos_meta:
            messagebox.showwarning("Faltan elementos", "Debes colocar la hormiga y el hongo antes de continuar.")
            return
        
        matrizCostos = self.entorno.obtenerMatrizCostos()
        beta = None
        
        # Get beta value for beam search
        if algoritmo == "beam":
            try:
                beta = int(self.entry_filas.get())
                if beta <= 0:
                    messagebox.showwarning("Error", "El valor de β debe ser mayor que 0")
                    return
            except ValueError:
                messagebox.showwarning("Error", "Por favor ingrese un valor válido para β")
                return
        
        self.destroy()
        simulador = Simulador(self.entorno, algoritmo, matrizCostos, beta)
        simulador.mainloop()
