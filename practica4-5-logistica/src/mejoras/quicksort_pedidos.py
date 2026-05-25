# src/mejoras/quicksort_pedidos.py
# Mejora 5 (Tema 3): Quicksort personalizado para ordenar pedidos
# por múltiples criterios (beneficio, urgencia, densidad de valor).

def quicksort_pedidos(pedidos, criterio="densidad", ascendente=False):
    """
    Ordena pedidos con Quicksort recursivo según el criterio elegido.

    Criterios disponibles:
      "densidad"  → beneficio / peso   (ratio de valor por kg)
      "beneficio" → beneficio absoluto
      "peso"      → peso del pedido
      "volumen"   → volumen del pedido

    Complejidad Teórica: 
      - Caso Medio / Mejor Caso: O(N log N) gracias a la mediana de 3.
      - Peor Caso: O(N^2).

    :param pedidos: lista de dicts.
    :param criterio: clave de ordenación.
    :param ascendente: True = menor primero.
    :return: nueva lista ordenada.
    """
    # CASO BASE (Divide y Vencerás): Una lista de 0 o 1 elementos ya está ordenada por definición.
    if len(pedidos) <= 1:
        return pedidos

    # Función auxiliar para extraer el valor de comparación según el criterio sin usar Objetos.
    def clave(p):
        if criterio == "densidad":
            return p.get("beneficio", 0) / max(p.get("peso", 1), 1)
        return p.get(criterio, 0)

    # 1. FASE DE DIVISIÓN: Elección del Pivote (Mediana de tres)
    # Seleccionamos el primer, central y último elemento. Al usar la mediana de estos tres
    # evitamos que el algoritmo degenere a O(N^2) si le pasamos una lista que ya venía ordenada.
    primero, central, ultimo = pedidos[0], pedidos[len(pedidos)//2], pedidos[-1]
    
    # Este sorted interno opera siempre sobre exactamente 3 elementos, por lo que su complejidad es O(1) constante.
    candidatos = sorted([primero, central, ultimo], key=clave)
    pivote_val = clave(candidatos[1])

    # 2. FASE DE PARTICIÓN O(N): 
    # Separamos el array en tres sub-arrays recorriendo la lista original una sola vez.
    menores = [p for p in pedidos if clave(p) < pivote_val]
    iguales = [p for p in pedidos if clave(p) == pivote_val]
    mayores = [p for p in pedidos if clave(p) > pivote_val]

    # 3. FASE DE CONQUISTA Y COMBINACIÓN:
    # Llamadas recursivas sobre los sub-problemas (menores y mayores).
    # La concatenación final (+) une las soluciones parciales en la solución global.
    ordenado = (quicksort_pedidos(menores, criterio, ascendente) +
                iguales +
                quicksort_pedidos(mayores, criterio, ascendente))

    # Inversión condicional O(N) si se solicita un orden descendente.
    return ordenado if ascendente else list(reversed(ordenado))


def imprimir_ranking(pedidos, criterio="densidad"):
    """
    Muestra el ranking de pedidos según el criterio establecido.
    Útil para la justificación del algoritmo voraz que depende de una lista previamente ordenada.
    """
    labels = {
        "densidad": "Densidad de valor (ben/kg)",
        "beneficio": "Beneficio (€)",
        "peso": "Peso (kg)",
        "volumen": "Volumen (m³)",
    }
    
    # Ejecutamos nuestro algoritmo de divide y vencerás
    ordenados = quicksort_pedidos(pedidos, criterio)
    
    print(f"\n[ MEJORA 5: RANKING POR {labels.get(criterio, criterio).upper()} ]")
    print(f"  {'#':>3} | {'ID':>4} | {'Destino':<20} | {'Peso':>6} | {'Vol':>5} | {'Ben':>6} | {'Ben/kg':>8}")
    print(f"  {'-'*3}-+-{'-'*4}-+-{'-'*20}-+-{'-'*6}-+-{'-'*5}-+-{'-'*6}-+-{'-'*8}")
    
    for i, p in enumerate(ordenados, 1):
        den = p.get("beneficio", 0) / max(p.get("peso", 1), 1)
        print(f"  {i:>3} | {p['id']:>4} | {p.get('destino','?'):<20} | "
              f"{p.get('peso',0):>6} | {p.get('volumen',0):>5} | "
              f"{p.get('beneficio',0):>6} | {den:>8.2f}")