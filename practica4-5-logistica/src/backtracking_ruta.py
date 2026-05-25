# src/backtracking_ruta.py
# Módulo de Optimización de Ruta (TSP Híbrido)
# Combina ramificación y poda con programación dinámica exacta .
# Incluye gestión de LIFO, recálculo de rutas con Floyd-Warshall y mecanismos de seguridad (Timeout).

import math
import time

LIMITE_DESTINOS = 10    # Límite teórico: por encima de este número (O(10!) = 3.6 millones), se usa Held-Karp
TIMEOUT_SEGUNDOS = 5    # Mecanismo de seguridad para evitar cuelgues del sistema en la evaluación


def calcular_coste_arista(arista):
    """
    Normaliza el valor heurístico de la arista. Si el grafo tiene distancia y tiempo,
    los combina linealmente para crear un único coste de optimización.
    """
    if arista == 0 or arista == [0, 0]:
        return 0
    if isinstance(arista, (int, float)):
        return arista
    if isinstance(arista, (list, tuple)):
        return arista[0] + arista[1]
    return float('inf')


def floyd_warshall(grafo):
    """
    Calcula el camino mínimo entre todos los pares de nodos mediante programación dinámica.
    Devuelve la matriz de costes y la de siguientes para reconstruir rutas reales.
    
    Análisis de Complejidad:
      - Tiempo: O(V^3) (Triple bucle anidado).
      - Espacio: O(V^2) para almacenar las distancias y los predecesores.
    """
    n = len(grafo)
    dist = [[math.inf] * n for _ in range(n)]
    siguiente = [[None] * n for _ in range(n)]

    # 1. Inicialización de Casos Base
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
                siguiente[i][j] = i
            else:
                coste = calcular_coste_arista(grafo[i][j])
                dist[i][j] = coste
                if coste != math.inf:
                    siguiente[i][j] = j

    # 2. Relación de Recurrencia
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Si pasar por el nodo intermedio 'k' mejora el coste directo de 'i' a 'j'
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    # Actualizamos el puntero para saber por dónde desviarnos
                    siguiente[i][j] = siguiente[i][k]

    return dist, siguiente


def reconstruir_camino_completo(ruta_entregas, matriz_siguiente):
    """
    Expande la secuencia de paradas del TSP en el camino físico calle a calle.
    Si el TSP dice que hay que ir del Almacén a FAR, esta función 
    reconstruye el trazado exacto usando la matriz de Floyd-Warshall.
    """
    camino = []
    if not ruta_entregas:
        return camino
        
    for i in range(len(ruta_entregas) - 1):
        origen  = ruta_entregas[i]
        destino = ruta_entregas[i + 1]
        if matriz_siguiente[origen][destino] is None:
            continue
            
        actual = origen
        while actual != destino:
            if not camino or camino[-1] != actual:
                camino.append(actual)
            actual = matriz_siguiente[actual][destino]
            
    camino.append(ruta_entregas[-1])
    return camino


def _held_karp(matriz_costes, nodos_destinos):
    """
    TSP exacto por programación dinámica con Bitmask.
    Se activa automáticamente para evitar la explosión factorial del Backtracking puro.

    Justificación:
      - Estado: dp[mask][i] = coste mínimo para salir del almacén, 
        visitar exactamente los nodos representados en binario en 'mask', y terminar en 'i'.
      - Recurrencia: dp[mask | (1<<j)][j] = min(dp[mask][i] + d(i,j))
      - Complejidad: Pasa de O(n!) del Backtracking a O(n^2 * 2^n) en tiempo, sacrificando O(n * 2^n) de memoria. 
    """
    n   = len(nodos_destinos)
    INF = math.inf
    idx_a_nodo = list(nodos_destinos)

    # La máscara de bits (1 << n) representa todos los subconjuntos posibles de destinos
    dp   = [[INF] * n for _ in range(1 << n)]
    pred = [[-1]  * n for _ in range(1 << n)]

    # Caso base: Distancia directa desde el almacén (0) a cada destino individual
    for i, nodo in enumerate(idx_a_nodo):
        dp[1 << i][i] = matriz_costes[0][nodo]

    # Transiciones de estado
    for mask in range(1 << n):
        for i in range(n):
            # Si el nodo 'i' no está en la máscara actual o no es alcanzable, ignoramos
            if not (mask & (1 << i)) or dp[mask][i] == INF:
                continue
            nodo_i = idx_a_nodo[i]
            
            for j in range(n):
                # Si el nodo 'j' ya fue visitado en esta máscara, lo saltamos
                if mask & (1 << j):
                    continue
                nodo_j    = idx_a_nodo[j]
                nuevo     = mask | (1 << j)
                nuevo_c   = dp[mask][i] + matriz_costes[nodo_i][nodo_j]
                
                # Si encontramos un subcamino mejor, actualizamos
                if nuevo_c < dp[nuevo][j]:
                    dp[nuevo][j]   = nuevo_c
                    pred[nuevo][j] = i

    # Cierre del ciclo: Volver al almacén (Nodo 0) desde el último nodo visitado
    full       = (1 << n) - 1
    mejor_c    = INF
    ultimo_idx = -1
    for i in range(n):
        c = dp[full][i] + matriz_costes[idx_a_nodo[i]][0]
        if c < mejor_c:
            mejor_c    = c
            ultimo_idx = i

    # Traceback: Reconstruir ruta deshaciendo la máscara de bits
    ruta_idx = []
    mask = full
    cur  = ultimo_idx
    while cur != -1:
        ruta_idx.append(cur)
        anterior = pred[mask][cur]
        mask ^= (1 << cur)
        cur = anterior
    ruta_idx.reverse()

    ruta = [0] + [idx_a_nodo[i] for i in ruta_idx] + [0]
    return mejor_c, ruta


def calcular_ruta_optima(grafo, nodos_a_visitar, pila_lifo_destinos, usar_poda=True):
    """
    Enrutador principal. Decide inteligentemente la estrategia algorítmica en función del tamaño de la entrada.
    
    :return: (coste, paradas_entrega, camino_fisico, nodos_explorados)
    """
    # 1. Precálculo de distancias reales en el mapa
    matriz_costes, matriz_siguiente = floyd_warshall(grafo)

    # 2. Control de explosión combinatoria
    if len(nodos_a_visitar) > LIMITE_DESTINOS:
        print(f"  [!] {len(nodos_a_visitar)} destinos superan el limite ({LIMITE_DESTINOS}).")
        print("      Usando Held-Karp (DP exacta) en lugar de backtracking.")
        coste, ruta = _held_karp(matriz_costes, nodos_a_visitar)
        camino = reconstruir_camino_completo(ruta, matriz_siguiente)
        return coste, ruta, camino, -1

    # 3. Preparación de variables para Backtracking puro
    mejor_coste          = math.inf
    mejor_ruta_entregas  = []
    nodos_explorados     = 0
    inicio               = time.perf_counter()
    timeout_alcanzado    = False

    def backtrack(nodo_actual, pendientes, ruta_actual, coste_acum, stack):
        nonlocal mejor_coste, mejor_ruta_entregas, nodos_explorados, timeout_alcanzado

        # Poda temporal de emergencia
        if time.perf_counter() - inicio > TIMEOUT_SEGUNDOS:
            timeout_alcanzado = True
            return

        nodos_explorados += 1

        # PODA: Cortamos la rama si el coste parcial ya supera al mejor coste global
        if usar_poda and coste_acum >= mejor_coste:
            return

        # CASO BASE: Todos los paquetes entregados, volvemos al origen
        if not pendientes:
            coste_final = coste_acum + matriz_costes[nodo_actual][0]
            if coste_final < mejor_coste:
                mejor_coste         = coste_final
                mejor_ruta_entregas = ruta_actual + [0]
            return

        # RAMIFICACIÓN: Permutamos sobre los destinos restantes
        for i in range(len(pendientes)):
            if timeout_alcanzado:
                return
                
            siguiente    = pendientes[i]
            
            # Penalización heurística LIFO: +15 de coste si obligamos al repartidor 
            # a extraer un paquete que no está en la puerta de la furgoneta.
            penalizacion = 15 if (stack and siguiente != stack[-1]) else 0
            
            # Simulamos la extracción del paquete del sistema LIFO
            nuevo_stack  = [s for s in stack if s != siguiente]
            
            # Descenso recursivo en profundidad
            backtrack(
                siguiente,
                pendientes[:i] + pendientes[i + 1:],
                ruta_actual + [siguiente],
                coste_acum + matriz_costes[nodo_actual][siguiente] + penalizacion,
                nuevo_stack
            )

    # Llamada inicial desde el almacén (Nodo 0)
    backtrack(0, nodos_a_visitar, [0], 0, pila_lifo_destinos)

    if timeout_alcanzado:
        print(f"  [!] Timeout ({TIMEOUT_SEGUNDOS}s). Mejor solucion encontrada hasta el corte.")

    # Reconstrucción final del trazado calle a calle
    camino_fisico = reconstruir_camino_completo(mejor_ruta_entregas, matriz_siguiente)
    return mejor_coste, mejor_ruta_entregas, camino_fisico, nodos_explorados