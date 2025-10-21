
# Documentación — Beam Search (implementación con registro detallado)

Beam Search es una estrategia de búsqueda informada que equilibra eficiencia y precisión mediante la exploración parcial del espacio de estados. A diferencia de una búsqueda exhaustiva (como A* o BFS), este algoritmo limita la cantidad de nodos activos en cada iteración según un parámetro denominado β (beta), lo que reduce significativamente el uso de memoria.

La implementación incluida cuenta con un sistema de registro detallado (`log_info`) que documenta cada iteración: expansiones, costos y decisiones. Esto facilita la integración con GUIs o cajas de texto (TextBox) para depuración y animación.

## Contenido

- Idea principal y motivación
- Parámetros
- Flujo del algoritmo
- Heurística
- Estructura del registro (`log_info`)
- Complejidad y comportamiento

## 1. Idea principal y motivación

En cada iteración se evalúan todos los caminos actuales en la `frontera` según su función de costo total:

$$f(n)=g(n)+h(n)$$

Solo se conservan los β caminos más prometedores; cada uno se expande a sus vecinos válidos y se registran métricas de la iteración (nodos expandidos, frontera, costos, etc.). Este enfoque prioriza nodos con menor costo estimado y evita un crecimiento incontrolado de la frontera, siendo adecuado para visualizaciones y simulaciones interactivas.

## 2. Parámetros

- `entorno`: instancia de la clase `Entorno` que debe proveer:
	- `matriz`: `List[List[int]]` que representa el mapa.
	- `pos_hormiga`: tupla `(x, y)` con la posición inicial.
	- `pos_meta`: tupla `(x, y)` con la posición objetivo.
- `beta` (int): ancho del haz — número máximo de caminos que se mantienen por iteración.
- `matrizCostos` (opcional): `List[List[int]]` con costos por celda (por defecto, costo uniforme = 1).

## 3. Flujo del algoritmo

### 3.1 Inicialización

- Obtener la matriz y sus dimensiones.
- Calcular valores iniciales:

	- `g(inicio) = 0`
	- `h(inicio) = distancia_manhattan(inicio, meta)`
	- `f(inicio) = g(inicio) + h(inicio)`

- Inicializar la frontera:

```python
frontera = [(f_inicio, g_inicio, [inicio])]
```

- Crear estructuras auxiliares:
	- `visitados`: conjunto de posiciones ya exploradas.
	- `pasos`: lista de trazas detalladas.
	- `log_info`: diccionario para registrar parámetros, métricas y estados.

### 3.2 Bucle principal

Mientras la `frontera` no esté vacía:

1. Selección de los mejores β caminos: ordenar la frontera y conservar los β más prometedores.

```python
frontera = sorted(frontera, key=lambda x: x[0])[:beta]
```

2. Expansión de nodos: para cada camino seleccionado:

- Tomar el último nodo como `actual`.
- Si `actual == meta`, registrar el éxito y retornar `(camino, pasos, log_info)`.
- Si `actual` ya fue visitado, saltar.
- Generar vecinos válidos (arriba, abajo, izquierda, derecha):

```python
vecinos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
```

- Para cada `vecino` válido calcular:

	- `g_nuevo = g_actual + costo_mov` (por defecto 1 o tomado de `matrizCostos`)
	- `h_nuevo = heuristica_manhattan(vecino, pos_meta)`
	- `f_nuevo = g_nuevo + h_nuevo`

	Insertar el nuevo camino en la nueva frontera (por ejemplo con `heapq.heappush`).

3. Registro de decisiones: por cada expansión se guarda información relevante:

```json
{
	"pos": actual,
	"accion": "Expandir nodo",
	"decisiones": [(pos_vecino, f_vecino, g_vecino, h_vecino), ...],
	"iteracion": iteracion,
	"f_actual": f_actual,
	"g_actual": g_actual,
	"h_actual": h_actual,
	"nodos_visitados": len(visitados)
}
```

4. Actualización de la frontera: seleccionar los mejores β caminos del heap:

```python
frontera = [heappop(nueva_frontera) for _ in range(min(beta, len(nueva_frontera)))]
```

5. Registrar en `log_info["iteraciones"]` la información de la iteración (frontera inicial, nodos expandidos, resumen estadístico, etc.).

### 3.3 Criterios de parada

- Meta alcanzada: si se encuentra un nodo con `h == 0`, retornar el camino, `pasos` y `log_info` con `log_info["resultado"] = "meta_alcanzada"`.
- Frontera vacía: si no hay más nodos por explorar, establecer:

```python
log_info["resultado"] = "sin_solucion"
log_info["razon"] = "frontera_vacia"
```

## 4. Heurística: distancia Manhattan

Se utiliza la distancia Manhattan, apropiada para movimientos ortogonales en cuadrícula:

$$h(a,b)=|a_x-b_x|+|a_y-b_y|$$

```python
def heuristica_manhattan(a, b):
		"""Calcula la distancia Manhattan entre dos puntos (fila, columna)."""
		return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

## 5. Estructura del registro (`log_info`)

`log_info` contiene la trazabilidad completa del proceso. Campos importantes:

- `inicio`, `meta`: posiciones inicial y final.
- `beta`: valor del haz usado.
- `iteraciones`: lista con información por iteración (cada entrada incluye frontera, expandidos, decisiones, estadísticas).
- `g_inicio`, `h_inicio`, `f_inicio`: valores iniciales.
- `resultado`: `"sin_solucion"` o `"meta_alcanzada"`.
- `total_iteraciones`: número total de iteraciones ejecutadas.
- `total_visitados`: cantidad de nodos distintos explorados.

Ejemplo de uso de `log_info`:

```python
log_info = {
		"inicio": inicio,
		"meta": meta,
		"beta": beta,
		"iteraciones": [],
		"g_inicio": g_inicio,
		"h_inicio": h_inicio,
		"f_inicio": f_inicio,
}
```

## 6. Complejidad y comportamiento

- Complejidad temporal aproximada: O(β ⋅ b ⋅ d)
	- `b`: factor de ramificación (promedio de vecinos por nodo).
	- `d`: profundidad máxima (profundidad de la solución).
	- `β`: tamaño del haz.

- Complejidad espacial: O(β ⋅ d)

### Ventajas

- Reduce drásticamente el consumo de memoria frente a A*.
- Permite animaciones interactivas y análisis paso a paso mediante `log_info`.

### Desventajas

- Puede perder la solución óptima si `β` es demasiado pequeño.
- El rendimiento depende fuertemente de la calidad de la heurística.
