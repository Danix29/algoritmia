# src/tests/test_backtracking.py
# Pruebas unitarias para el módulo de optimización de ruta (Backtracking y Floyd-Warshall).
# Valida la corrección matemática, el cumplimiento de restricciones del TSP y la eficacia de la poda.

import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtracking_ruta import calcular_ruta_optima, floyd_warshall

# Grafo de prueba reducido para validaciones deterministas.
# Formato: [distancia_m, tiempo_min]. Es simétrico y completo.
GRAFO_TEST = [
    [[0, 0.0],   [500, 6.0], [800, 9.5], [600, 7.1], [900, 10.7]],
    [[500, 6.0],  [0, 0.0],  [300, 3.6], [400, 4.8], [700, 8.3]],
    [[800, 9.5],  [300, 3.6], [0, 0.0],  [350, 4.2], [200, 2.4]],
    [[600, 7.1],  [400, 4.8], [350, 4.2], [0, 0.0],  [450, 5.4]],
    [[900, 10.7], [700, 8.3], [200, 2.4], [450, 5.4], [0, 0.0]],
]


def test_un_solo_destino():
    """
    Verifica el comportamiento del algoritmo de Backtracking en su caso más trivial (N=1).
    Asegura que las recursiones y casos base no fallen en escenarios de mínima profundidad.
    """
    coste, paradas, camino, nodos = calcular_ruta_optima(
        GRAFO_TEST, [1], [1]
    )
    assert paradas == [0, 1, 0]
    assert coste > 0
    assert nodos > 0


def test_poda_no_cambia_optimo():
    """
    Verifica el principio fundamental de ramificación y poda.
    A diferencia de las heurísticas voraces, la poda por cota superior es un método EXACTO.
    Garantiza que descartar ramas nunca elimina la solución óptima del árbol de estados.
    """
    _, paradas_sin, _, _ = calcular_ruta_optima(
        GRAFO_TEST, [1, 2, 3], [1, 2, 3], usar_poda=False
    )
    _, paradas_con, _, _ = calcular_ruta_optima(
        GRAFO_TEST, [1, 2, 3], [1, 2, 3], usar_poda=True
    )
    
    # Calculamos la distancia pura para verificar que ambas rutas miden lo mismo
    coste_sin = sum(
        GRAFO_TEST[paradas_sin[i]][paradas_sin[i+1]][0]
        for i in range(len(paradas_sin)-1)
    )
    coste_con = sum(
        GRAFO_TEST[paradas_con[i]][paradas_con[i+1]][0]
        for i in range(len(paradas_con)-1)
    )
    assert coste_sin == coste_con


def test_poda_reduce_nodos():
    """
    Comprueba empíricamente la eficiencia de la poda.
    El número de nodos explorados (tamaño del árbol de recursión) usando poda 
    siempre debe ser menor o igual que en la fuerza bruta pura O(N!).
    """
    _, _, _, n_sin = calcular_ruta_optima(
        GRAFO_TEST, [1, 2, 3, 4], [1, 2, 3, 4], usar_poda=False
    )
    _, _, _, n_con = calcular_ruta_optima(
        GRAFO_TEST, [1, 2, 3, 4], [1, 2, 3, 4], usar_poda=True
    )
    assert n_con <= n_sin


def test_ruta_empieza_y_termina_en_almacen():
    """
    Comprueba la restricción fundamental del problema de ruteo (TSP): 
    El recorrido debe ser un ciclo cerrado que nace y muere obligatoriamente en el origen (Nodo 0).
    """
    _, paradas, _, _ = calcular_ruta_optima(
        GRAFO_TEST, [1, 2], [1, 2]
    )
    assert paradas[0] == 0
    assert paradas[-1] == 0


def test_visita_todos_los_destinos():
    """
    Garantiza que el algoritmo construye un camino que incluye sin excepciones
    todo el subconjunto de destinos seleccionados por la mochila.
    """
    destinos = [1, 2, 3]
    _, paradas, _, _ = calcular_ruta_optima(GRAFO_TEST, destinos, destinos)
    for d in destinos:
        assert d in paradas


def test_floyd_warshall_diagonal_cero():
    """
    Verifica el caso base de inicialización en la matriz de programación dinámica 
    de Floyd-Warshall: el coste de ir de un nodo a sí mismo siempre es estrictamente 0.
    """
    dist, _ = floyd_warshall(GRAFO_TEST)
    for i in range(len(GRAFO_TEST)):
        assert dist[i][i] == 0


def test_floyd_warshall_simetrico():
    """
    Valida la coherencia de los caminos mínimos. Dado que el grafo urbano original 
    es simétrico (grafo no dirigido), la matriz de costes mínimos calculada por DP
    también debe serlo (con tolerancia a errores de precisión de punto flotante).
    """
    dist, _ = floyd_warshall(GRAFO_TEST)
    n = len(GRAFO_TEST)
    for i in range(n):
        for j in range(n):
            assert abs(dist[i][j] - dist[j][i]) < 1e-9


if __name__ == "__main__":
    # Ejecuta dinámicamente todas las funciones que empiezan por 'test_'
    for nombre, func in list(globals().items()):
        if nombre.startswith("test_") and callable(func):
            try:
                func()
                print(f"  OK  {nombre}")
            except AssertionError as e:
                print(f"  FALLO  {nombre}: {e}")