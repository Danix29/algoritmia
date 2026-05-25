# src/utils/generador_escenarios.py
# Mejora 1 (Tema 1): Generador Recursivo de Escenarios .
# Genera instancias de prueba dinámicas utilizando recursividad pura.
# Además, precalcula las distancias reales del campus usando Floyd-Warshall para garantizar 
# que los escenarios cumplan la desigualdad triangular.

import json
import math
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOPO_PATH  = os.path.join(SCRIPT_DIR, "..", "topologia_uah.json")

# Nodos físicos del campus científico de la UAH
EDIFICIOS_UAH = ["ENF", "MED", "HOS", "FAR", "AMB", "QUI", "RES", "BOT", "CIE"]


def _cargar_topologia():
    """Carga el grafo base del campus desde un archivo JSON local."""
    ruta = os.path.normpath(TOPO_PATH)
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def _floyd_warshall(nodos, aristas):
    """
    Calcula las distancias mínimas entre todos los pares de nodos del campus.
    Garantiza que si no hay calle directa entre A y B, el generador asigne la distancia del camino indirecto más corto.

    Análisis de programación dinámica:
      - Estado: dist[i][j] es la distancia mínima entre i y j.
      - Caso base: dist[i][i] = 0 (distancia al mismo nodo).
      - Recurrencia: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
      - Complejidad: O(V^3) en tiempo, O(V^2) en espacio.
    """
    n   = len(nodos)
    idx = {nid: i for i, nid in enumerate(nodos)}
    INF = math.inf

    # Inicialización de matrices (distancia y tiempo)
    dist  = [[INF] * n for _ in range(n)]
    t_mat = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i]  = 0
        t_mat[i][i] = 0.0

    # Llenado con las aristas directas existentes
    for e in aristas:
        i, j = idx[e["origen"]], idx[e["destino"]]
        dist[i][j]  = dist[j][i]  = e["distancia_m"]
        t_mat[i][j] = t_mat[j][i] = e["tiempo_min"]

    # Triple bucle de optimización
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j]  = dist[i][k] + dist[k][j]
                    t_mat[i][j] = t_mat[i][k] + t_mat[k][j]

    return dist, t_mat


def _construir_subgrafo(nodos_subset, dist, t_mat, idx_global):
    """
    Extrae una sub-matriz de adyacencia (grafo completo) solo para los edificios que participan en los pedidos generados.
    """
    k = len(nodos_subset)
    g = []
    for i in range(k):
        fila = []
        for j in range(k):
            gi = idx_global[nodos_subset[i]]
            gj = idx_global[nodos_subset[j]]
            fila.append([int(dist[gi][gj]), round(t_mat[gi][gj], 1)])
        g.append(fila)
    return g


def generar_pedidos_recursivos(edificios, id_actual=0, pedidos=None):
    """
    Genera pedidos de forma recursiva con destinos reales del campus UAH.

    - Caso base: id_actual >= len(edificios) -> devuelve la lista acumulada.
    - Caso recursivo: crea un pedido con el edificio actual y hace la llamada con id+1.
    """
    if pedidos is None:
        pedidos = []
        
    # CASO BASE: Se ha asignado un pedido a cada edificio solicitado
    if id_actual >= len(edificios):
        return pedidos
        
    # CASO RECURSIVO: Generamos el pedido actual
    pedidos.append({
        "id":        id_actual + 1,
        "destino":   edificios[id_actual],
        "peso":      random.randint(1, 6),
        "volumen":   round(random.randint(1, 5) * 0.5, 1),
        "beneficio": random.randint(10, 100),
    })
    
    # Llamada recursiva avanzando el estado (id_actual + 1)
    return generar_pedidos_recursivos(edificios, id_actual + 1, pedidos)


def _serializar_escenario(escenario):
    """
    Serializa el diccionario a un JSON de texto con un formateo personalizado para que sea humanamente legible.
    """
    grafo   = escenario["grafo"]
    sin_grafo = {k: v for k, v in escenario.items() if k != "grafo"}

    base = json.dumps(sin_grafo, indent=2, ensure_ascii=False)
    base = base.rstrip("\n}")

    # Formateo visual de la matriz del grafo
    filas_str = []
    for fila in grafo:
        aristas = ", ".join(f"[{a[0]},{a[1]}]" for a in fila)
        filas_str.append(f"    [{aristas}]")
    grafo_str = "[\n" + ",\n".join(filas_str) + "\n  ]"

    # Formateo compacto para los diccionarios de pedidos
    for pedido in escenario["pedidos"]:
        viejo = json.dumps(pedido, indent=2, ensure_ascii=False)
        nuevo = json.dumps(pedido, ensure_ascii=False)
        base  = base.replace(viejo, nuevo)

    return base + ',\n  "grafo": ' + grafo_str + "\n}"


def generar_escenario_unico(num_pedidos):
    """
    Función orquestadora. Genera un JSON completo combinando los pedidos recursivos y el subgrafo de Floyd-Warshall.
    """
    # Evitar superar el número máximo de edificios disponibles
    num_pedidos = min(num_pedidos, len(EDIFICIOS_UAH))

    topo    = _cargar_topologia()
    nodos_g = [n["id"] for n in topo["nodos"]]
    idx_g   = {nid: i for i, nid in enumerate(nodos_g)}
    dist, t_mat = _floyd_warshall(nodos_g, topo["caminos"])

    edificios_sel   = random.sample(EDIFICIOS_UAH, num_pedidos)
    nodos_escenario = ["EPS"] + edificios_sel # EPS actúa como el Almacén / Base

    # Llamada a la lógica recursiva y de subgrafos
    pedidos = generar_pedidos_recursivos(edificios_sel)
    grafo   = _construir_subgrafo(nodos_escenario, dist, t_mat, idx_g)

    # Restricciones globales de la mochila
    cap_peso = random.randint(num_pedidos * 2, num_pedidos * 4)
    cap_vol  = float(random.randint(num_pedidos * 3, num_pedidos * 6))

    escenario = {
        "nombre":            f"Escenario Autogenerado (N={num_pedidos})",
        "descripcion":       f"{num_pedidos} pedidos en el campus UAH generados recursivamente.",
        "peso_furgoneta":    cap_peso,
        "volumen_furgoneta": cap_vol,
        "nodos":             nodos_escenario,
        "pedidos":           pedidos,
        "grafo":             grafo,
    }

    # Guardado dinámico en la estructura de directorios del proyecto
    ruta = os.path.normpath(
        os.path.join(SCRIPT_DIR, "..", "data", "escenarios", "escenario_generado.json")
    )
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(_serializar_escenario(escenario))

    print(f"  Escenario guardado en: {ruta}")


if __name__ == "__main__":
    generar_escenario_unico(6)