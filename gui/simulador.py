import tkinter as tk
from tkinter import scrolledtext, messagebox
from core.algoritmo_beam import beam_search, heuristica_manhattan
from core.algoritmo_dynamic import dynamic_weight_a_star


class Simulador(tk.Tk):
    def __init__(self, entorno, algoritmo, matrizCostos=None, beta=None):
        super().__init__()

        self.entorno = entorno
        self.algoritmo = algoritmo
        self.matrizCostos = matrizCostos
        self.beta = beta
        self.title(f"Simulador - {algoritmo.upper()}")
        self.geometry("1200x700")
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
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(frame_derecho, text="Siguiente paso", bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold"), command=self.siguiente_paso).pack(pady=10, fill=tk.X)
        tk.Button(frame_derecho, text="Resolver todo", bg="#2196F3", fg="white",
                  font=("Arial", 12, "bold"), command=self.resolver_todo).pack(pady=10, fill=tk.X)

        tk.Label(frame_derecho, text="Registro de decisiones:",
                 bg="#ececec", font=("Arial", 12, "bold")).pack(pady=10)
        self.text_area = scrolledtext.ScrolledText(frame_derecho, width=60, height=35, wrap=tk.WORD,
                                                    font=("Courier", 9))
        self.text_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # --- Información inicial ---
        self.text_area.insert(tk.END, "="*60 + "\n")
        self.text_area.insert(tk.END, "INICIO DE BEAM SEARCH\n")
        self.text_area.insert(tk.END, "="*60 + "\n")
        self.text_area.insert(tk.END, f"Algoritmo seleccionado: {algoritmo.upper()}\n")
        self.text_area.insert(tk.END, f"Posición inicial: {entorno.pos_hormiga}\n")
        self.text_area.insert(tk.END, f"Posición meta: {entorno.pos_meta}\n")
        if self.beta:
            self.text_area.insert(tk.END, f"Beta (ancho de haz): {self.beta}\n")
        self.text_area.insert(tk.END, f"Tamaño del mapa: {entorno.filas}x{entorno.columnas}\n")
        self.text_area.insert(tk.END, f"Usando matriz de costos: {'Sí' if matrizCostos else 'No'}\n")
        
        # Calcular valores iniciales
        if entorno.pos_hormiga and entorno.pos_meta:
            g_inicio = 0
            h_inicio = heuristica_manhattan(entorno.pos_hormiga, entorno.pos_meta)
            f_inicio = g_inicio + h_inicio
            self.text_area.insert(tk.END, f"\nEstado inicial:\n")
            self.text_area.insert(tk.END, f"  g(inicio) = {g_inicio}\n")
            self.text_area.insert(tk.END, f"  h(inicio) = {h_inicio}\n")
            self.text_area.insert(tk.END, f"  f(inicio) = {f_inicio}\n")
        
        self.text_area.insert(tk.END, "="*60 + "\n\n")

        # --- Ejecutar el algoritmo seleccionado ---
        self.ruta = []
        self.pasos = []
        self.log_info = None
        self.paso_actual = 0

        if algoritmo == "beam":
            resultado = beam_search(entorno, self.beta, self.matrizCostos)
            if resultado[0]:
                self.ruta, self.pasos, self.log_info = resultado
                self.text_area.insert(tk.END, f"✓ Ruta calculada con éxito.\n")
                self.text_area.insert(tk.END, f"  Total de nodos en la ruta: {len(self.ruta)}\n\n")
                # Mostrar toda la información usando el log
                self.mostrar_log_completo()
            else:
                # Capturar log incluso si no hay solución
                self.log_info = resultado[2] if len(resultado) > 2 else None
                self.text_area.insert(tk.END, "✗ No se encontró camino con Beam Search.\n\n")
                if self.log_info:
                    self.mostrar_log_completo()
                else:
                    messagebox.showinfo("Sin resultado", "No se encontró camino con Beam Search.")
        
        elif algoritmo == "dynamic":
            resultado = dynamic_weight_a_star(entorno)
            if resultado[0]:
                self.ruta, self.pasos = resultado
                self.text_area.insert(tk.END, f"✓ Ruta calculada con éxito.\n")
                self.text_area.insert(tk.END, f"  Total de nodos en la ruta: {len(self.ruta)}\n\n")
            else:
                messagebox.showinfo("Sin resultado", "No se encontró camino con Dynamic Weight A*.")
        else:
            messagebox.showinfo("Aviso", f"Algoritmo {algoritmo} aún no implementado.")

        self.dibujar_mapa()

    def dibujar_mapa(self):
        """Dibuja el mapa con la ruta actual"""
        self.canvas.delete("all")
        for i in range(self.entorno.filas):
            for j in range(self.entorno.columnas):
                x1, y1 = j * self.celda_size, i * self.celda_size
                x2, y2 = x1 + self.celda_size, y1 + self.celda_size
                valor = self.entorno.matriz[i][j]

                color = "white"
                if valor == "H" and self.paso_actual > 0:
                    color = "orange"
                elif valor == "V":
                    color = "red"
                elif valor == "M":
                    color = "green"

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill=color)

        # Dibujar la posición actual de la hormiga
        if self.paso_actual < len(self.ruta):
            fila, col = self.ruta[self.paso_actual]
            x1, y1 = col * self.celda_size, fila * self.celda_size
            x2, y2 = x1 + self.celda_size, y1 + self.celda_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange", width=3)

    def mostrar_log_completo(self):
        """Muestra toda la información del algoritmo usando el log estructurado"""
        if not self.log_info:
            return
        
        # Mostrar información de cada iteración
        for iter_info in self.log_info.get("iteraciones", []):
            if iter_info["tipo"] == "meta_alcanzada":
                self.text_area.insert(tk.END, "\n" + "="*60 + "\n")
                self.text_area.insert(tk.END, "¡META ALCANZADA!\n")
                self.text_area.insert(tk.END, "="*60 + "\n")
                self.text_area.insert(tk.END, f"Camino final: {iter_info['camino_final']}\n")
                self.text_area.insert(tk.END, f"Longitud del camino: {iter_info['longitud']}\n")
                self.text_area.insert(tk.END, f"Costo total: {iter_info['costo_total']}\n")
                self.text_area.insert(tk.END, f"Iteraciones realizadas: {iter_info['numero']}\n")
                self.text_area.insert(tk.END, "="*60 + "\n\n")
            
            elif iter_info["tipo"] == "expansion":
                self.text_area.insert(tk.END, "\n" + "─"*60 + "\n")
                self.text_area.insert(tk.END, f"ITERACIÓN {iter_info['numero']}\n")
                self.text_area.insert(tk.END, "─"*60 + "\n")
                
                # Mostrar frontera inicial
                self.text_area.insert(tk.END, f"\nFrontera actual (después del corte con beta={self.beta}):\n")
                for i, nodo_front in enumerate(iter_info['frontera_inicial'], 1):
                    self.text_area.insert(tk.END, 
                        f"  {i}. Nodo: {nodo_front['nodo']}, f={nodo_front['f']}, "
                        f"g={nodo_front['g']}, h={nodo_front['h']}, camino: {nodo_front['camino']}\n")
                
                # Mostrar cada nodo expandido
                for nodo_exp in iter_info['nodos_expandidos_detalle']:
                    self.text_area.insert(tk.END, f"\n  → Expandiendo nodo: {nodo_exp['nodo']}\n")
                    self.text_area.insert(tk.END, 
                        f"    f={nodo_exp['f']}, g={nodo_exp['g']}, h={nodo_exp['h']}\n")
                    
                    if nodo_exp['vecinos']:
                        self.text_area.insert(tk.END, f"    Explorando vecinos:\n")
                        for vecino in nodo_exp['vecinos']:
                            self.text_area.insert(tk.END, 
                                f"      • {vecino['pos']}: costo_mov={vecino['costo_mov']}, "
                                f"g={vecino['g']}, h={vecino['h']}, f={vecino['f']}\n")
                        self.text_area.insert(tk.END, 
                            f"    ✓ Vecinos válidos expandidos: {nodo_exp['vecinos_validos']}\n")
                
                # Mostrar resumen de la iteración
                resumen = iter_info['resumen']
                self.text_area.insert(tk.END, f"\n  Resumen iteración {iter_info['numero']}:\n")
                self.text_area.insert(tk.END, f"    • Nodos expandidos: {resumen['nodos_expandidos']}\n")
                self.text_area.insert(tk.END, f"    • Tamaño nueva frontera: {resumen['tamano_nueva_frontera']}\n")
                self.text_area.insert(tk.END, f"    • Nodos visitados total: {resumen['nodos_visitados']}\n")
        
        # Mostrar resultado final si no hay solución
        if self.log_info.get("resultado") == "sin_solucion":
            self.text_area.insert(tk.END, "\n" + "="*60 + "\n")
            if self.log_info.get("razon") == "frontera_vacia":
                self.text_area.insert(tk.END, "BÚSQUEDA TERMINADA SIN ENCONTRAR SOLUCIÓN\n")
                self.text_area.insert(tk.END, f"Frontera vacía en iteración {self.log_info.get('total_iteraciones', '?')}\n")
            else:
                self.text_area.insert(tk.END, "NO SE ENCONTRÓ CAMINO A LA META\n")
            self.text_area.insert(tk.END, f"Iteraciones realizadas: {self.log_info.get('total_iteraciones', 0)}\n")
            self.text_area.insert(tk.END, f"Nodos visitados: {self.log_info.get('total_visitados', 0)}\n")
            self.text_area.insert(tk.END, "="*60 + "\n\n")
        
        self.text_area.see(tk.END)

    def siguiente_paso(self):
        """Avanza la hormiga un paso en la ruta"""
        if not self.ruta:
            messagebox.showinfo("Aviso", "No hay ruta para mostrar.")
            return

        if self.paso_actual < len(self.ruta) - 1:
            self.paso_actual += 1
            self.dibujar_mapa()
        else:
            messagebox.showinfo("Completado", "¡La hormiga ha llegado a la meta!")

    def resolver_todo(self):
        """Mueve la hormiga automáticamente por toda la ruta"""
        if not self.ruta:
            messagebox.showinfo("Aviso", "No hay ruta calculada.")
            return

        # Mover al final de la ruta
        self.paso_actual = len(self.ruta) - 1
        self.dibujar_mapa()
        messagebox.showinfo("Completado", f"¡Ruta completada! Total de pasos: {len(self.ruta)}")