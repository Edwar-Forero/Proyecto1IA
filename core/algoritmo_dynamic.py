from heapq import heappush, heappop
from math import inf
from core.entorno import Entorno


def heuristica_manhattan(a, b):
    """Calcula la distancia Manhattan entre dos puntos."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dynamic_weight_a_star(entorno: Entorno, epsilon: float = 1.5):
    """
    Implementación de Dynamic Weight A*.
    f(n) = g(n) + h(n) + ε * (1 - d(n)/N) * h(n)
    """

    mapa = entorno.matriz
    filas, columnas = len(mapa), len(mapa[0])

    inicio = entorno.pos_hormiga
    meta = entorno.pos_meta

    if not inicio or not meta:
        raise ValueError("Mapa inválido: falta la hormiga o el hongo mágico.")

    # Inicialización
    N = filas + columnas  # profundidad máxima estimada
    frontera = []
    heappush(frontera, (0, inicio, [inicio], 0))  # (f, nodo, camino, profundidad)
    g_cost = {inicio: 0}
    visitados = set()
    pasos = []

    while frontera:
        f_actual, actual, camino, profundidad = heappop(frontera)

        if actual in visitados:
            continue
        visitados.add(actual)

        pasos.append({
            "pos": actual,
            "accion": "Expandir nodo",
            "frontera": frontera.copy(),
            "decisiones": []
        })

        if actual == meta:
            pasos.append({
                "pos": actual,
                "accion": "Meta alcanzada 🎯",
                "frontera": frontera.copy()
            })
            return camino, pasos

        # Vecinos en las 4 direcciones
        vecinos = [
            (actual[0] - 1, actual[1]),  # arriba
            (actual[0] + 1, actual[1]),  # abajo
            (actual[0],     actual[1] - 1),  # izquierda
            (actual[0],     actual[1] + 1)   # derecha
        ]

        for nx, ny in vecinos:
            if 0 <= nx < filas and 0 <= ny < columnas:
                celda = mapa[nx][ny]

                # --- Determinar costo del terreno ---
                # P = camino normal → costo 1
                # V = veneno → costo alto (p.ej. 5)
                # H = hongo (meta) → costo 1
                # M = hormiga → costo 1
                if celda == "V":
                    costo = 5  # alto, pero permitido
                else:
                    costo = 1

                vecino = (nx, ny) 
                g_nuevo = g_cost[actual] + costo
                h_nuevo = heuristica_manhattan(vecino, meta)
                d = profundidad + 1

                # Peso dinámico de la heurística
                f_nuevo = g_nuevo + h_nuevo + epsilon * (1 - (d / N)) * h_nuevo

                pasos[-1]["decisiones"].append((vecino, f_nuevo))

                if vecino not in g_cost or g_nuevo < g_cost[vecino]:
                    g_cost[vecino] = g_nuevo
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    heappush(frontera, (f_nuevo, vecino, nuevo_camino, d))

    pasos.append({
        "pos": None,
        "accion": "No se encontró camino ❌",
        "frontera": []
    })
    return None, pasos
