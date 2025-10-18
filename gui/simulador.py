import tkinter as tk
from tkinter import scrolledtext, messagebox
from core.algoritmo_beam import beam_search


class Simulador(tk.Tk):
    def __init__(self, entorno, algoritmo, matrizCostos=None, beta=None):
        super().__init__()

        self.entorno = entorno
        self.algoritmo = algoritmo
        self.matrizCostos = matrizCostos
        self.beta = beta
        self.title(f"Simulador - {algoritmo.upper()}")
        self.geometry("1000x700")
        self.configure(bg="#f9f9f9")

        self.celda_size = 40
        self.canvas = tk.Canvas(
            self,
            bg="white",
            width=self.entorno.columnas * self.celda_size,
            height=self.entorno.filas * self.celda_size
        )
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)

        # --- Panel derecho ---
        frame_derecho = tk.Frame(self, bg="#ececec")
        frame_derecho.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Button(frame_derecho, text="Siguiente paso", bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold"), command=self.siguiente_paso).pack(pady=10, fill=tk.X)
        tk.Button(frame_derecho, text="Resolver todo", bg="#2196F3", fg="white",
                  font=("Arial", 12, "bold"), command=self.resolver_todo).pack(pady=10, fill=tk.X)

        tk.Label(frame_derecho, text="Registro de decisiones:",
                 bg="#ececec", font=("Arial", 12, "bold")).pack(pady=10)
        self.text_area = scrolledtext.ScrolledText(frame_derecho, width=40, height=25, wrap=tk.WORD)
        self.text_area.pack(padx=5, pady=5)

        self.text_area.insert(tk.END, f"Algoritmo seleccionado: {algoritmo}\n")
        self.text_area.insert(tk.END, f"Hormiga en: {entorno.pos_hormiga}\n")
        self.text_area.insert(tk.END, f"Hongo en: {entorno.pos_meta}\n\n")

        # --- Ejecutar el algoritmo seleccionado ---
        self.ruta = []
        self.pasos = []
        self.paso_actual = 0

        if algoritmo == "beam":
            resultado = beam_search(entorno, self.beta, self.matrizCostos)
            if resultado[0]:
                self.ruta, self.pasos = resultado
                self.text_area.insert(tk.END, f"Ruta calculada con éxito. Total pasos: {len(self.ruta)}\n\n")
            else:
                messagebox.showinfo("Sin resultado", "No se encontró camino con Beam Search.")
        else:
            messagebox.showinfo("Aviso", f"Algoritmo {algoritmo} aún no implementado.")

        self.dibujar_mapa()

    # -----------------------------
    # Dibuja el mapa con la ruta actual
    # -----------------------------
    def dibujar_mapa(self):
        self.canvas.delete("all")
        for i in range(self.entorno.filas):
            for j in range(self.entorno.columnas):
                x1, y1 = j * self.celda_size, i * self.celda_size
                x2, y2 = x1 + self.celda_size, y1 + self.celda_size
                valor = self.entorno.matriz[i][j]

                color = "white"
                if valor == "H" and self.paso_actual > 0:  # Hormiga
                    color = "orange"
                elif valor == "V":  # Veneno
                    color = "red"
                elif valor == "M":  # Meta
                    color = "green"

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=color)

        # Dibujar la posición actual de la hormiga (si hay ruta)
        if self.paso_actual < len(self.ruta):
            fila, col = self.ruta[self.paso_actual]
            x1, y1 = col * self.celda_size, fila * self.celda_size
            x2, y2 = x1 + self.celda_size, y1 + self.celda_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange")

    # -----------------------------
    # Mostrar un paso a la vez
    # -----------------------------
    def siguiente_paso(self):
        if not self.ruta:
            self.text_area.insert(tk.END, "No hay ruta para mostrar.\n")
            return

        if self.paso_actual < len(self.ruta):
            pos_actual = self.ruta[self.paso_actual]
            
            # Obtener información del paso actual
            if self.paso_actual < len(self.pasos):
                paso_info = self.pasos[self.paso_actual]
                
                # Mostrar información detallada
                self.text_area.insert(tk.END, f"\n=== Paso {self.paso_actual + 1} ===\n")
                self.text_area.insert(tk.END, f" Posición actual: {paso_info['pos']}\n")
                
                if 'decisiones' in paso_info:
                    self.text_area.insert(tk.END, "\n Nodos explorados:\n")
                    for decision in paso_info['decisiones']:
                        pos, costo = decision
                        self.text_area.insert(tk.END, f"  → {pos} (costo total: {costo})\n")
                
                if 'frontera' in paso_info:
                    self.text_area.insert(tk.END, "\n Frontera antes del corte:\n")
                    for nodo in paso_info['frontera']:
                        self.text_area.insert(tk.END, f"  • Costo: {nodo[0]}, Camino: {nodo[1]}\n")

            self.paso_actual += 1
            self.dibujar_mapa()
            self.text_area.see(tk.END)  # Auto-scroll
        else:
            self.text_area.insert(tk.END, "\n ¡Ruta completada!\n")

    # -----------------------------
    # Resolver todo el camino de una vez
    # -----------------------------
    def resolver_todo(self):
        if not self.ruta:
            self.text_area.insert(tk.END, "No hay ruta calculada.\n")
            return

        self.text_area.insert(tk.END, "\n--- Resolviendo todo el recorrido ---\n")
        for i, (fila, col) in enumerate(self.ruta):
            self.text_area.insert(tk.END, f"Paso {i + 1}: {fila, col}\n")

        self.text_area.insert(tk.END, " Ruta completa mostrada.\n")
        self.paso_actual = len(self.ruta) - 1
        self.dibujar_mapa()
