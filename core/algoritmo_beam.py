# core/algoritmo_beam.py
from heapq import heappush, heappop
from core.entorno import Entorno


def heuristica_manhattan(a, b):
    """Calcula la distancia Manhattan entre dos puntos."""
    distancia = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distancia


def beam_search(entorno: Entorno, beta: int, matrizCostos=None):
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
    pasos = []

    def es_valido(x, y, camino_actual):
        # Verificamos que la posición sea válida y que no esté en el camino actual
        valido = (0 <= x < filas and 0 <= y < columnas and 
                 (x, y) not in camino_actual)
        return valido

    iteracion = 1
    while frontera:
        frontera = sorted(frontera, key=lambda x: x[0])[:beta]
        nueva_frontera = []

        for _, camino in frontera:
            actual = camino[-1]

            if heuristica_manhattan(actual, meta) == 0:
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

            decisiones = []
            camino_actual = set(camino)  # Convertimos el camino a set para búsqueda O(1)
            
            for nx, ny in vecinos:
                if not es_valido(nx, ny, camino_actual):
                    continue
                    
                costo_mov = 1
                if matrizCostos:
                    costo_mov = matrizCostos[nx][ny]
                
                nuevo_camino = list(camino)
                nuevo_camino.append((nx, ny))
                h = heuristica_manhattan((nx, ny), meta) + costo_mov
                heappush(nueva_frontera, (h, nuevo_camino))
                decisiones.append(((nx, ny), h))

            pasos.append({
                "pos": actual,
                "accion": "Expandir nodo",
                "decisiones": decisiones,
                "frontera": frontera.copy()
            })

        frontera = [heappop(nueva_frontera) for _ in range(min(beta, len(nueva_frontera)))]
        iteracion += 1

    return None, pasos
