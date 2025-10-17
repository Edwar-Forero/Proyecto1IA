# core/algoritmo_beam.py
from heapq import heappush, heappop
from core.entorno import Entorno


def heuristica_manhattan(a, b):
    """Calcula la distancia Manhattan entre dos puntos."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def beam_search(entorno: Entorno, beta: int):
    """
    Ejecuta Beam Search sobre el entorno actual.
    Retorna el camino y una lista de pasos (para animación paso a paso).
    """
    mapa = entorno.matriz
    filas, columnas = len(mapa), len(mapa[0])

    inicio = entorno.pos_hormiga
    meta = entorno.pos_meta

    if not inicio or not meta:
        raise ValueError("Mapa inválido: falta la hormiga o el hongo mágico.")

    frontera = [(heuristica_manhattan(inicio, meta), [inicio])]
    visitados = set()
    pasos = []  # para registrar decisiones paso a paso

    while frontera:
        frontera = sorted(frontera, key=lambda x: x[0])[:beta]
        nueva_frontera = []

        for _, camino in frontera:
            actual = camino[-1]

            if actual == meta:
                pasos.append({
                    "pos": actual,
                    "accion": "Meta alcanzada 🎯",
                    "frontera": frontera.copy()
                })
                return camino, pasos

            if actual in visitados:
                continue
            visitados.add(actual)

            vecinos = [
                (actual[0] - 1, actual[1]),  # arriba
                (actual[0] + 1, actual[1]),  # abajo
                (actual[0], actual[1] - 1),  # izquierda
                (actual[0], actual[1] + 1)   # derecha
            ]

            # Analizar cada vecino
            decisiones = []
            for nx, ny in vecinos:
                if 0 <= nx < filas and 0 <= ny < columnas:
                    if mapa[nx][ny] != "V":  # evitar veneno
                        nuevo_camino = list(camino)
                        nuevo_camino.append((nx, ny))
                        h = heuristica_manhattan((nx, ny), meta)
                        heappush(nueva_frontera, (h, nuevo_camino))
                        decisiones.append(((nx, ny), h))

            pasos.append({
                "pos": actual,
                "accion": "Expandir nodo",
                "decisiones": decisiones,
                "frontera": frontera.copy()
            })

        # Seleccionar los β más prometedores
        frontera = [heappop(nueva_frontera) for _ in range(min(beta, len(nueva_frontera)))]

    return None, pasos
