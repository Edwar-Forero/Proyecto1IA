# Documentación — Dynamic Weight A\* (Implementación)

**Dynamic Weight A\*** es una variante del algoritmo A\* que ajusta dinámicamente los pesos sobre la heurística con el objetivo de realizar una búsqueda más informada y rápida a medida que se acerca a la meta.

---

## 1. Idea principal y motivación

El A\* estándar utiliza la función de evaluación:

$$
f(n) = g(n) + h(n)
$$

En entornos grandes, las búsquedas a menudo necesitan **priorizar exploración al inicio** (rápida) y **explotación al final** (precisa).

Para lograrlo, se emplea un **término multiplicador variable** sobre la heurística, que disminuye con la profundidad del nodo.  
Así, la heurística tiene más influencia en los nodos cercanos al inicio y menos en los lejanos (o viceversa, según el diseño).

La versión implementada utiliza:

$$
f(n) = g(n) + h(n) + \varepsilon \cdot \left(1 - \frac{d(n)}{N}\right) \cdot h(n)
$$

donde:

- \( g(n) \): costo acumulado desde el inicio hasta el nodo \( n \).
- \( h(n) \): heurística (Manhattan) desde \( n \) hasta la meta.
- \( \varepsilon \): parámetro (peso dinámico base) ≥ 0.
- \( d(n) \): profundidad del nodo \( n \) (número de pasos desde el inicio).
- \( N \): cota estimada de la profundidad máxima (en la implementación: filas + columnas).

El término \( \varepsilon(1 - d/N)h(n) \) incrementa inicialmente la influencia de la heurística y la reduce conforme crece la profundidad \( d \).

---

## Parámetros

- **entorno**: instancia de la clase `Entorno` que debe exponer al menos:

  - `matriz`: estructura tipo `List[List[Celda]]` que representa el mapa (rejilla).
  - `pos_hormiga`: tupla `(fila, columna)` — posición inicial.
  - `pos_meta`: tupla `(fila, columna)` — posición objetivo.

- **epsilon**: `float` (por defecto `1.5`) — factor de peso dinámico.

---

## Flujo del algoritmo (pasos)

1. **Validación inicial**

   - Extraer dimensiones (`filas`, `columnas`), posición de inicio (`pos_hormiga`) y meta (`pos_meta`).
   - Validar que ambas posiciones estén dentro de la `matriz` y que las celdas sean transitables.

2. **Inicialización**

   - Calcular la cota:
     $$
     N = \text{filas} + \text{columnas}
     $$
   - Inicializar la **frontera** como un _min-heap_; cada entrada contendrá tuplas del tipo `(f, nodo, camino, profundidad)`.
   - Inicializar `g_cost` como diccionario: costo \(g\) mejor conocido por cada posición.
   - Inicializar `visitados` como conjunto vacío.
   - Insertar el nodo inicial en la frontera con:
     $$
     g(\text{inicio}) = 0,\quad d(\text{inicio}) = 0
     $$

3. **Bucle principal**

   - Mientras `frontera` no esté vacía:

     1. Extraer (heappop) la entrada con menor \(f\).
     2. Si el `nodo` está en `visitados`, continuar.
     3. Marcar `nodo` como visitado.
     4. Si `nodo` == `pos_meta`: reconstruir y retornar el `camino`.
     5. Generar vecinos válidos (4 direcciones: arriba, abajo, izquierda, derecha).
     6. Para cada `vecino`:
        - Calcular `costo` del movimiento (según la celda o costo de transición).
        - Calcular:
          $$
          g_{\text{nuevo}} = g(\text{actual}) + \text{costo}
          $$
          $$
          h_{\text{nuevo}} = \text{heuristica\_manhattan}(\text{vecino}, \text{meta})
          $$
          $$
          d = \text{profundidad actual} + 1
          $$
          $$
          f_{\text{nuevo}} = g_{\text{nuevo}} + h_{\text{nuevo}} + \varepsilon \cdot \left(1 - \frac{d}{N}\right) \cdot h_{\text{nuevo}}
          $$
        - Si `g_nuevo` < `g_cost[vecino]` (o `vecino` no está en `g_cost`):
          - Actualizar `g_cost[vecino] = g_nuevo`.
          - Insertar `(f_nuevo, vecino, nuevo_camino, d)` en la `frontera`.

   - Si la frontera se vacía sin encontrar la meta → **no hay solución**; retornar `None` o estructura equivalente.

---

## 4. Complejidad y comportamiento

- En el peor caso (por ejemplo \(\varepsilon \approx 0\), heurística admisible), el algoritmo se comporta como A\* y la complejidad temporal puede ser **exponencial** en la profundidad de la solución:

  $$
  O(b^d)
  $$

  donde \(b\) es el factor de ramificación promedio y \(d\) la profundidad (longitud) de la solución.

- En la práctica, la heurística y el control de `visitados` reducen drásticamente la exploración en mapas razonables.

- **Efecto del término dinámico** $$\varepsilon\cdot(1 - d/N)\cdot h(n) $$
  - Aumenta la influencia de la heurística en niveles iniciales (cuando \(d\) es pequeño), acelerando la búsqueda hacia la región prometedora.
  - Reduce esa influencia al acercarse a profundidades mayores, favoreciendo la explotación local y evitando sesgos excesivos.
  - Riesgo: si \(\varepsilon\) es muy grande o la fórmula se ajusta mal, puede inducir soluciones subóptimas en mapas con costes no homogéneos.
