# src/mejoras/floyd_warshall.py
# Mejora 7 (Propuesta avanzada): Floyd-Warshall
# Precalcula las distancias mínimas reales entre TODOS los pares de nodos del campus UAH.
# Útil cuando el grafo NO es completo (hay aristas faltantes o rutas indirectas más cortas).
# El backtracking opera ya sobre la matriz resultante de este preprocesado.

import math

def calcular_coste_arista(arista):
    """
    Normaliza cualquier formato de arista a un float único.
    Soporta: 0, [0,0], int, float, [dist_m, tiempo_min].
    """
    if arista == 0 or arista == [0, 0]:
        return 0.0
    if isinstance(arista, (int, float)):
        return float(arista)
    if isinstance(arista, (list, tuple)) and len(arista) >= 2:
        # Combina distancia (metros) + tiempo (minutos * escala) en un coste único.
        # Usamos dist_m / 100 + tiempo_min para mantener unidades comparables.
        return arista[0] / 100 + arista[1]
    return math.inf


def floyd_warshall(grafo):
    """
    Calcula el camino mínimo entre todos los pares de nodos.

    Estado: dist[i][j] = mínimo coste para ir de i a j.
    Recurrencia: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    Casos base: dist[i][i] = 0; dist[i][j] = coste_arista(grafo[i][j]).
    Complejidad: O(V^3) tiempo | O(V^2) espacio.

    :param grafo: matriz de adyacencia con aristas en formato [dist_m, tiempo_min].
    :return: matriz de costes mínimos entre todos los pares.
    """
    n = len(grafo)
    dist = [[math.inf] * n for _ in range(n)]

    # 1. Inicialización de la matriz de distancias
    for i in range(n):
        for j in range(n):
            dist[i][j] = 0.0 if i == j else calcular_coste_arista(grafo[i][j])

    # 2. Triple bucle anidado
    # En cada paso k, actualizamos la tabla para permitir que el nodo 'k' forme parte del camino.
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Evaluamos el coste de ir de 'i' a 'j' pasando por 'k'.
                via_k = dist[i][k] + dist[k][j]
                # Si el camino indirecto es más barato, actualizamos el mínimo.
                if via_k < dist[i][j]:
                    dist[i][j] = via_k

    return dist


def floyd_warshall_con_caminos(grafo):
    """
    Versión extendida que además reconstruye el camino mínimo entre cada par.
    Vital para conocer la ruta alternativa cuando ocurre un corte de calle en el Backtracking.

    :return: (matriz_dist, matriz_pred) donde pred[i][j] es el nodo anterior en el camino mínimo de i a j (None si no hay camino).
    """
    n = len(grafo)
    dist = [[math.inf] * n for _ in range(n)]
    pred = [[None] * n for _ in range(n)]

    # Inicialización simultánea de distancias y predecesores.
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0.0
            else:
                c = calcular_coste_arista(grafo[i][j])
                dist[i][j] = c
                if c < math.inf:
                    pred[i][j] = i  # Inicialmente, el predecesor de 'j' es 'i' (camino directo)

    # Relación de recurrencia aplicada a distancias y a la tabla de predecesores.
    for k in range(n):
        for i in range(n):
            for j in range(n):
                via_k = dist[i][k] + dist[k][j]
                if via_k < dist[i][j]:
                    dist[i][j] = via_k
                    pred[i][j] = pred[k][j]

    return dist, pred


def reconstruir_camino(pred, origen, destino):
    """Devuelve la lista de nodos del camino mínimo de origen a destino."""
    # Si la celda es None, el nodo es inalcanzable (ej. grafo desconectado)
    if pred[origen][destino] is None:
        return []
    camino = [destino]
    actual = destino
    # Reconstruimos hacia atrás saltando por los predecesores
    while actual != origen:
        actual = pred[origen][actual]
        camino.append(actual)
    # Invertimos la lista para mostrar el orden cronológico (Origen -> ... -> Destino)
    return list(reversed(camino))


def imprimir_matriz(dist, nodos):
    """Print de la matriz de distancias."""
    print("\n[ MEJORA 7: MATRIZ FLOYD-WARSHALL (costes mínimos) ]")
    ancho = 8
    cabecera = f"{'':>{ancho}}" + "".join(f"{n:>{ancho}}" for n in nodos)
    print(cabecera)
    for i, ni in enumerate(nodos):
        fila = f"{ni:>{ancho}}" + "".join(
            f"{'inf':>{ancho}}" if dist[i][j] == math.inf
            else f"{dist[i][j]:>{ancho}.1f}"
            for j in range(len(nodos))
        )
        print(fila)