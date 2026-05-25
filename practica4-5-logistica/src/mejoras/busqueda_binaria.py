# src/mejoras/busqueda_binaria.py
# Mejora 6 (Tema 3): Búsqueda binaria sobre la capacidad de peso.
# Encuentra la menor capacidad C tal que la mochila 3D alcance al menos un porcentaje X% del beneficio máximo posible.

import sys
import os
# Se añade el directorio padre al path para importar el módulo de programación dinámica
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dp_seleccion import seleccionar_pedidos_dp


def capacidad_minima_para_porcentaje(pedidos, porcentaje, cap_vol, cap_peso_max=None):
    """
    Búsqueda binaria sobre cap_peso para encontrar la menor capacidad que
    garantiza alcanzar 'porcentaje'% del beneficio máximo posible.

    :param pedidos: lista de dicts con peso, volumen, beneficio.
    :param porcentaje: 0..100 (ej. 80 = «80 % del beneficio máximo»).
    :param cap_vol: capacidad de volumen fija del vehículo.
    :param cap_peso_max: límite superior de búsqueda (suma total de pesos si None).
    :return: (cap_minima, beneficio_obtenido, pedidos_seleccionados)
    """
    # Caso base: si no hay pedidos o el porcentaje es nulo, no se requiere capacidad.
    if not pedidos or porcentaje <= 0:
        return 0, 0, []
    
    # Si no se proporciona un límite superior, el máximo teórico es la suma de todos los pesos.
    if cap_peso_max is None:
        cap_peso_max = sum(int(p.get("peso", 0)) for p in pedidos)

    # Calcular el beneficio máximo posible usando la capacidad máxima.
    ben_max, _ = seleccionar_pedidos_dp(pedidos, cap_peso_max, cap_vol)
    objetivo = ben_max * porcentaje / 100

    # Inicialización de punteros para la búsqueda binaria (Divide y Vencerás)
    # Espacio de búsqueda: desde 0 kg hasta cap_peso_max kg.
    lo, hi = 0, cap_peso_max
    mejor_c = cap_peso_max
    mejor_ben = ben_max
    mejor_eleg = []

    # Bucle principal
    while lo <= hi:
        mid = (lo + hi) // 2
        # Evaluamos el rendimiento de la mochila con la capacidad 'mid'
        ben, eleg = seleccionar_pedidos_dp(pedidos, mid, cap_vol)
        if ben >= objetivo:
            # Si cumplimos el objetivo, guardamos esta capacidad como la mejor actual.
            mejor_c = mid
            mejor_ben = ben
            mejor_eleg = eleg
            # Como queremos minimizar la capacidad, podamos la mitad superior y buscamos en [lo, mid - 1]
            hi = mid - 1   # intentar con menos capacidad
        else:
            # Si no llegamos al objetivo, necesitamos más capacidad. Podamos la mitad inferior.
            lo = mid + 1

    return mejor_c, mejor_ben, mejor_eleg


def imprimir_tabla_capacidades(pedidos, cap_vol, cap_peso_actual):
    """Muestra tabla de capacidad mínima para diferentes objetivos porcentuales."""
    print("\n[ MEJORA 6: BÚSQUEDA BINARIA — CAPACIDAD MÍNIMA POR OBJETIVO ]")
    print(f"  Capacidad actual del vehículo: {cap_peso_actual} kg\n")
    print(f"  {'%Obj':>5} | {'C_min (kg)':>10} | {'Beneficio':>10} | Pedidos seleccionados")
    print(f"  {'-'*5}-+-{'-'*10}-+-{'-'*10}-+-{'-'*30}")

    # Evalúa escalonadamente distintos umbrales para demostrar la flexibilidad del algoritmo
    for pct in [50, 70, 80, 90, 95, 100]:
        c, b, eleg = capacidad_minima_para_porcentaje(pedidos, pct, cap_vol, cap_peso_actual)
        # Extrae los IDs de forma funcional para mantener la salida limpia
        ids = sorted(p["id"] for p in eleg)
        print(f"  {pct:>4}% | {c:>10} | {b:>9} € | {ids}")