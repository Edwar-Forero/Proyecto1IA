from heapq import heappush, heappop
from core.entorno import Entorno


def heuristica_manhattan(a, b):
    """Calcula la distancia Manhattan entre dos puntos."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def beam_search(entorno: Entorno, beta: int, matrizCostos=None):
    
    mapa = entorno.matriz # Obtener el mapa del entorno
    filas, columnas = len(mapa), len(mapa[0]) # Obtener dimensiones del mapa
    inicio = entorno.pos_hormiga
    meta = entorno.pos_meta

    if not inicio or not meta:
        raise ValueError("Mapa inválido: falta la hormiga o el hongo mágico.")

    # Log de información completa, para TextBox
    log_info = {
        "inicio": inicio,
        "meta": meta,
        "beta": beta,
        "filas": filas,
        "columnas": columnas,
        "usa_costos": matrizCostos is not None,
        "iteraciones": []
    }

    
    g_inicio = 0 # costo desde inicio a inicio es 0
    h_inicio = heuristica_manhattan(inicio, meta) # heurística desde inicio a meta
    f_inicio = g_inicio + h_inicio # f = g + h
    frontera = [(f_inicio, g_inicio, [inicio])] 
    visitados = set()
    pasos = []

    # Guardar estado inicial, para TextBox
    log_info["g_inicio"] = g_inicio
    log_info["h_inicio"] = h_inicio
    log_info["f_inicio"] = f_inicio

    def es_valido(x, y, camino_actual):
        return 0 <= x < filas and 0 <= y < columnas and (x, y) not in camino_actual # Evitar ciclos y fuera de límites

    iteracion = 0
    while frontera: # Mientras haya nodos en la frontera
        iteracion += 1
        
        # Ordenamos por f y limitamos a los mejores beta
        frontera = sorted(frontera, key=lambda x: x[0])[:beta] # Mantener solo los mejores beta
        
        # Guardar frontera actual
        frontera_info = []
        for f, g, cam in frontera:
            h = f - g
            frontera_info.append({
                "nodo": cam[-1],
                "f": f,
                "g": g,
                "h": h,
                "camino": cam
            })
        
        nueva_frontera = []
        nodos_expandidos = 0
        nodos_por_iteracion = []

        for f_actual, g_actual, camino in frontera:
            actual = camino[-1]
            h_actual = f_actual - g_actual

            # Verificar si se ha alcanzado la meta
            if heuristica_manhattan(actual, meta) == 0:
                log_info["iteraciones"].append({
                    "numero": iteracion,
                    "tipo": "meta_alcanzada",
                    "nodo": actual,
                    "f": f_actual,
                    "g": g_actual,
                    "h": h_actual,
                    "camino_final": camino,
                    "longitud": len(camino),
                    "costo_total": g_actual
                })
                
                pasos.append({
                    "pos": actual,
                    "accion": "Meta alcanzada",
                    "decisiones": [],
                    "frontera": [(f, g, c) for f, g, c in frontera],
                    "iteracion": iteracion,
                    "camino": camino,
                    "g_actual": g_actual,
                    "f_actual": f_actual,
                    "h_actual": h_actual,
                    "nodos_visitados": len(visitados)
                })
                return camino, pasos, log_info

            if actual in visitados:
                continue
            
            visitados.add(actual)
            nodos_expandidos += 1

            vecinos = [
                (actual[0] - 1, actual[1]),  # arriba
                (actual[0] + 1, actual[1]),  # abajo
                (actual[0], actual[1] - 1),  # izquierda
                (actual[0], actual[1] + 1)   # derecha
            ]

            decisiones = []
            vecinos_validos = 0
            vecinos_info = []

            for nx, ny in vecinos:
                if not es_valido(nx, ny, set(camino)):
                    continue

                vecinos_validos += 1
                
                # Costo del movimiento
                costo_mov = 1
                if matrizCostos:
                    costo_mov = matrizCostos[nx][ny]

                g_nuevo = g_actual + costo_mov # Costo acumulado
                h = heuristica_manhattan((nx, ny), meta) # Heurística
                f_nuevo = g_nuevo + h # costo total

                nuevo_camino = list(camino) # Copiar camino actual
                nuevo_camino.append((nx, ny)) # Agregar nuevo nodo al camino

                heappush(nueva_frontera, (f_nuevo, g_nuevo, nuevo_camino)) # Agregar a la nueva frontera

                decisiones.append({
                    "pos": (nx, ny),
                    "g": g_nuevo,
                    "h": h,
                    "f": f_nuevo,
                    "costo_mov": costo_mov
                })
                
                vecinos_info.append({
                    "pos": (nx, ny),
                    "costo_mov": costo_mov,
                    "g": g_nuevo,
                    "h": h,
                    "f": f_nuevo
                })

            nodos_por_iteracion.append({
                "nodo": actual,
                "f": f_actual,
                "g": g_actual,
                "h": h_actual,
                "vecinos": vecinos_info,
                "vecinos_validos": vecinos_validos
            })

            pasos.append({
                "pos": actual,
                "accion": "Expandir nodo",
                "decisiones": decisiones,
                "frontera": [(f, g, c) for f, g, c in sorted(nueva_frontera, key=lambda x: x[0])[:beta]],
                "iteracion": iteracion,
                "f_actual": f_actual,
                "g_actual": g_actual,
                "h_actual": h_actual,
                "nodos_expandidos": nodos_expandidos,
                "vecinos_validos": vecinos_validos,
                "nodos_visitados": len(visitados),
                "tamano_nueva_frontera": len(nueva_frontera)
            })

        # Guardar información de la iteración completa, para TextBox
        log_info["iteraciones"].append({
            "numero": iteracion,
            "tipo": "expansion",
            "frontera_inicial": frontera_info,
            "nodos_expandidos_detalle": nodos_por_iteracion,
            "resumen": {
                "nodos_expandidos": nodos_expandidos,
                "tamano_nueva_frontera": len(nueva_frontera),
                "nodos_visitados": len(visitados)
            }
        })

        if not nueva_frontera:
            log_info["resultado"] = "sin_solucion"
            log_info["razon"] = "frontera_vacia"
            break

        # Extraemos los mejores beta elementos de la nueva frontera
        frontera = [heappop(nueva_frontera) for _ in range(min(beta, len(nueva_frontera)))]

    # Si no se llega a la meta, para textbox
    if not log_info.get("resultado"):
        log_info["resultado"] = "sin_solucion"
        log_info["razon"] = "no_encontrado"
    
    log_info["total_iteraciones"] = iteracion
    log_info["total_visitados"] = len(visitados)
    
    return None, pasos, log_info