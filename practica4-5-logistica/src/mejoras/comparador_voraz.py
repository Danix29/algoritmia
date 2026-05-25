# src/mejoras/comparador_voraz.py
# Mejora 3: Comparativa entre estrategias de resolución.

def seleccionar_pedidos_voraz(pedidos, cap_peso, cap_volumen):
    """
    Resuelve la mochila 3D de forma voraz ordenando por ratio beneficio/peso.
    No garantiza el optimo para la mochila 0/1, pero lo hace en O(N log N).

    :return: (beneficio_total, lista_seleccionados)
    """

    # Ordenamos los candidatos según la función heurística de maximización.
    # En este caso, priorizamos los paquetes que dan más beneficio por cada unidad de peso (ratio).
    # La complejidad de esta ordenación es O(N log N), lo cual es mucho más rápido que la matriz de DP.
    candidatos = sorted(pedidos, key=lambda p: p.get("beneficio", 0) / max(p.get("peso", 1), 1), reverse=True)
    seleccionados = []
    peso_usado = vol_usado = beneficio = 0

    # Recorremos la lista ordenada intentando meter cada paquete en la furgoneta. Complejidad de este bucle: O(N).  
    for p in candidatos:
        pp = int(p.get("peso", 0))
        pv = int(p.get("volumen", 0))
        pb = p.get("beneficio", 0)
        # Función de viabilidad: Comprobamos que el paquete actual no exceda las restricciones bidimensionales de la mochila (peso y volumen).
        if peso_usado + pp <= cap_peso and vol_usado + pv <= cap_volumen:
            seleccionados.append(p)
            peso_usado += pp
            vol_usado  += pv
            beneficio  += pb
    return beneficio, seleccionados


def comparar_voraz_vs_dp(pedidos, cap_peso, cap_volumen, beneficio_dp, elegidos_dp):
    """
    Ejecuta el voraz y devuelve las metricas de comparacion frente al optimo DP.
    :return: dict con beneficios, gap absoluto/relativo e ids de cada metodo.
    """
    # 1. Ejecutamos la aproximación Voraz
    beneficio_voraz, elegidos_voraz = seleccionar_pedidos_voraz(pedidos, cap_peso, cap_volumen)
    # 2. Análisis de métricas empíricas. Calculamos la diferencia exacta entre el globalmente óptimo (DP) y el óptimo local (Voraz).
    gap_abs = beneficio_dp - beneficio_voraz
    # Calculamos el porcentaje de pérdida para evaluar si la heurística voraz es "suficientemente buena"
    # en escenarios de capacidad crítica donde la DP tardaría demasiado tiempo en procesarse.
    gap_pct = (gap_abs / beneficio_dp * 100) if beneficio_dp > 0 else 0

    return {
        "beneficio_dp":      beneficio_dp,
        "beneficio_voraz":   beneficio_voraz,
        "gap_absoluto":      gap_abs,
        "gap_relativo_pct":  round(gap_pct, 2),
        "voraz_optimo":      beneficio_voraz == beneficio_dp,
        "ids_dp":            sorted(p["id"] for p in elegidos_dp),
        "ids_voraz":         sorted(p["id"] for p in elegidos_voraz),
    }


def imprimir_comparacion(comp):
    """
    Muestra los resultados de la métrica por consola.
    """
    print("\n[ MEJORA 3: COMPARADOR VORAZ vs DP ]")
    print(f"  DP    -> {comp['beneficio_dp']} EUR | pedidos {comp['ids_dp']}")
    print(f"  Voraz -> {comp['beneficio_voraz']} EUR | pedidos {comp['ids_voraz']}")
    
    # Comprobación de si el problema de la mochila 0/1 permitía que el Voraz fuera óptimo
    # (por coincidencia en la distribución de pesos y beneficios del caso concreto).
    if comp["voraz_optimo"]:
        print("  El voraz coincide con el optimo DP en este escenario.")
    else:
        print(f"  El voraz pierde {comp['gap_absoluto']} EUR "
              f"({comp['gap_relativo_pct']} % bajo el optimo).")