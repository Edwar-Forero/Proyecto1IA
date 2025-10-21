
## 1. Descripción general

La interfaz gráfica (GUI) del proyecto fue desarrollada completamente con **Tkinter**, y cumple la función de **visualizar, configurar y simular** el entorno donde la hormiga busca el camino hacia el hongo utilizando distintos algoritmos de búsqueda.  
El sistema GUI está compuesto por tres módulos principales:

- `ventana_inicio.py` → Configuración inicial del entorno.
- `editor_mapa.py` → Edición visual del mapa y selección del algoritmo.
- `simulador.py` → Ejecución y visualización paso a paso del algoritmo seleccionado.

El flujo de interacción está diseñado para que el usuario configure el tamaño del mapa, coloque los elementos del entorno y observe la ejecución del algoritmo elegido con retroalimentación visual y textual.

---

## 2. Ventana de inicio (`ventana_inicio.py`)

La primera interfaz permite al usuario ingresar el **número de filas y columnas** del mapa.  
Una vez ingresados, el botón **“Crear matriz”** genera un entorno vacío y abre el editor principal (`EditorMapa`).

### Funcionalidades clave
- Validación de entradas (solo enteros positivos).
- Cierre automático de la ventana inicial y apertura del editor.
- Interacción amigable y controlada del flujo.

**Propósito algorítmico:** preparar las dimensiones de la matriz donde se ejecutarán los algoritmos de búsqueda.

---

## 3. Editor del mapa (`editor_mapa.py`)

Esta ventana representa el **núcleo de la interacción entre el usuario y los algoritmos**.  
Permite construir visualmente el entorno donde se aplicará la búsqueda, colocando los elementos:

- **Hormiga (H)** → Nodo inicial.
- **Hongo (M)** → Nodo meta.
- **Veneno (V)** → Obstáculo o celda con costo elevado.
- **Borrar (❌)** → Elimina elementos colocados.

Cada tipo de celda se gestiona internamente mediante la clase `Entorno`, que mantiene una **matriz de estados** y genera la **matriz de costos** para los algoritmos.

### Botones principales de algoritmos
- **Usar Beam Search 🔍**  
  Permite ingresar un valor de **β (beta)**, que controla el **ancho de haz** o la cantidad máxima de nodos explorados por iteración.  
  Internamente llama al método:
  ```python
  self.iniciar_busqueda("beam")

Este algoritmo ajusta el peso dinámicamente según el progreso hacia la meta, buscando equilibrar velocidad y optimalidad.

Funcionalidades visuales

Dibujo dinámico de celdas mediante Canvas.

Colores diferenciados para cada tipo de celda (hormiga, meta, veneno, vacío).

Control del flujo de datos hacia el simulador.

Propósito algorítmico: definir el entorno y los parámetros que afectan el comportamiento de los algoritmos de búsqueda (costos, obstáculos, beta).

# Informe del módulo `simulador.py`  

## Descripción general

El módulo `simulador.py` implementa la ventana principal de simulación que **ejecuta y visualiza los algoritmos de búsqueda**:  
- **Beam Search (con parámetro β)**  
- **Dynamic Weighted A\***  

Esta interfaz permite observar en tiempo real el comportamiento de la hormiga al desplazarse desde su posición inicial hasta la meta (el hongo), mostrando tanto la **ruta óptima** como los **detalles de decisión internos** de cada algoritmo.

El objetivo del módulo es conectar la lógica de búsqueda (ubicada en `core/algoritmo_beam.py` y `core/algoritmo_dynamic.py`) con una **visualización interactiva** que facilite la comprensión del proceso de exploración y selección de caminos.

---

## Estructura general de la clase `Simulador`

La clase `Simulador` hereda de `tk.Tk`, convirtiéndose en una ventana principal independiente que puede instanciarse desde `editor_mapa.py` con los parámetros:

```python
Simulador(entorno, algoritmo, matrizCostos=None, beta=None)
