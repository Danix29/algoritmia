import json
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

from dp_seleccion import seleccionar_pedidos_dp
from backtracking_ruta import calcular_ruta_optima
from utils.generador_escenarios import generar_escenario_unico
from utils.visualizador import mostrar_ruta_ascii, mostrar_carga_lifo
from mejoras.comparador_voraz import comparar_voraz_vs_dp, imprimir_comparacion
from mejoras.floyd_warshall import imprimir_matriz, floyd_warshall_con_caminos
from mejoras.busqueda_binaria import imprimir_tabla_capacidades
from mejoras.quicksort_pedidos import imprimir_ranking

ESCENARIOS = {
    "1": "escenario_basico.json",
    "2": "escenario_capacidad_critica.json",
    "3": "escenario_ruteo_complejo.json",
    "4": "escenario_poda.json",
    "5": "escenario_libre.json",
}

def cargar_escenario(nombre_archivo):
    """Carga los datos estructurados del grafo y los pedidos desde el almacenamiento secundario."""
    ruta = os.path.join(SCRIPT_DIR, "data", "escenarios", nombre_archivo)
    if not os.path.exists(ruta):
        print(f"\n[!] No se encuentra: {ruta}")
        return None
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def ejecutar_escenario(datos):
    """
    Motor principal de simulacion logistica.
    Ejecuta secuencialmente los algoritmos de optimizacion y extrae metricas de complejidad empirica para cada fase del problema.
    """
    cap_peso     = datos.get("peso_furgoneta", datos.get("capacidad_furgoneta", 0))
    cap_vol      = datos.get("volumen_furgoneta", 0)
    pedidos_json = datos["pedidos"]
    grafo_ciudad = datos["grafo"]
    nodos        = datos.get("nodos", [])

    print(f" SIMULACION: {datos['nombre'].upper()}")

    # FASE 1: Carga de datos del escenario
    print("\n[ FASE 1: DATOS DEL VEHICULO Y PEDIDOS ]")
    print(f"  Capacidad: {cap_peso} kg | {cap_vol} m3")
    print("  Pedidos disponibles:")
    for p in pedidos_json:
        print(f"    {p.get('destino', '?'):20s} | {p.get('peso', 0)} kg | "
              f"{p.get('volumen', 0)} m3 | {p.get('beneficio', 0)} EUR")

    # FASE 2: Problema de la Mochila 0/1 (Programacion dinamica 3D)
    print("\n[ FASE 2: SELECCION DE PEDIDOS (Mochila 3D - DP) ]")
    t0 = time.perf_counter()
    beneficio_max, pedidos_elegidos = seleccionar_pedidos_dp(pedidos_json, cap_peso, cap_vol)
    t_dp = (time.perf_counter() - t0) * 1000

    print(f"  Beneficio optimo: {beneficio_max} EUR | t={t_dp:.4f} ms")
    peso_total = vol_total = 0
    for p in pedidos_elegidos:
        print(f"    ID {p['id']} | {p.get('destino', '?'):20s} | "
              f"{p['peso']} kg | {p.get('volumen', 0)} m3 | {p['beneficio']} EUR")
        peso_total += int(p["peso"])
        vol_total  += int(p.get("volumen", 0))
    print(f"  Uso: {peso_total}/{cap_peso} kg | {vol_total}/{cap_vol} m3")

    # Mejora 3: Heuristica voraz vs solucion exacta DP
    comp = comparar_voraz_vs_dp(pedidos_json, cap_peso, cap_vol, beneficio_max, pedidos_elegidos)
    imprimir_comparacion(comp)

    # Mejora 5: Quicksort multi-criterio para ranking de pedidos (Divide y Venceras)
    imprimir_ranking(pedidos_json, criterio="densidad")

    # FASE 3: Enrutamiento TSP (Floyd-Warshall + Backtracking con Poda)
    print("\n[ FASE 3: OPTIMIZACION DE RUTA (Floyd-Warshall + Backtracking) ]")

    if not pedidos_elegidos:
        print("  Sin pedidos seleccionados. La furgoneta permanece en el almacen.")
        return

    # Mejora 7: Precalculo de caminos minimos en el grafo no completo del campus UAH
    dist_fw, _ = floyd_warshall_con_caminos(grafo_ciudad)
    imprimir_matriz(dist_fw, nodos)

    nodos_destinos = []
    pila_lifo_ids  = []
    for pedido in pedidos_elegidos:
        dest = pedido.get("destino")
        idx  = nodos.index(dest) if dest in nodos else pedido.get("nodo_destino", 0)
        if idx not in nodos_destinos:
            nodos_destinos.append(idx)
        pila_lifo_ids.append(idx)

    # Comparacion empirica: Fuerza bruta O(n!) vs Ramificacion y poda
    t0 = time.perf_counter()
    _, _, _, n_brutos = calcular_ruta_optima(grafo_ciudad, nodos_destinos, pila_lifo_ids, usar_poda=False)
    t_bruta = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    mejor_coste, mejor_ruta, camino_fisico, n_poda = calcular_ruta_optima(grafo_ciudad, nodos_destinos, pila_lifo_ids, usar_poda=True)
    t_poda = (time.perf_counter() - t0) * 1000

    if n_brutos == -1:
        # Held-Karp activado automaticamente por superar el limite de destinos
        print(f"  Held-Karp (DP exacta): t={t_poda:.4f} ms")
    else:
        ratio = (1 - n_poda / n_brutos) * 100 if n_brutos else 0
        print(f"  SIN poda: {n_brutos} nodos | {t_bruta:.4f} ms")
        print(f"  CON poda: {n_poda} nodos | {t_poda:.4f} ms | reduccion {ratio:.1f}%")
    print(f"  Coste optimo (dist + tiempo + penalizacion LIFO): {mejor_coste:.1f}")

    # FASE 4: Logistica LIFO y visualizacion de la ruta
    print("\n[ FASE 4: LOGISTICA LIFO Y MAPA DE RUTA ]")
    orden_entrega = mejor_ruta[1:-1]
    paquetes_lifo = []
    for id_nodo in reversed(orden_entrega):
        nombre = nodos[id_nodo] if nodos else str(id_nodo)
        for p in pedidos_elegidos:
            if p.get("destino") == nombre:
                paquetes_lifo.append(p)
                break

    mostrar_ruta_ascii(mejor_ruta, nodos)
    mostrar_carga_lifo(paquetes_lifo)

    # FASE 5: Recalculo dinamico ante incidencia en la red viaria
    print("\n[ FASE 5: INCIDENCIA - RECALCULO CON FLOYD-WARSHALL ]")
    print("  Corte reportado: nodo 0 -> nodo 1.")

    grafo_mod = [row[:] for row in grafo_ciudad]
    grafo_mod[0][1] = [float("inf"), float("inf")]
    grafo_mod[1][0] = [float("inf"), float("inf")]

    t0 = time.perf_counter()
    coste_alt, ruta_alt, _, _ = calcular_ruta_optima(
        grafo_mod, nodos_destinos, nodos_destinos, usar_poda=True
    )
    t_rec = (time.perf_counter() - t0) * 1000
    ruta_alt_str = " -> ".join(nodos[i] if nodos else str(i) for i in ruta_alt)
    print(f"  Nuevo coste: {coste_alt:.1f} | Ruta alternativa: {ruta_alt_str}")
    print(f"  Tiempo de recalculo: {t_rec:.4f} ms")

    # Mejora 6: Busqueda Binaria sobre capacidad minima por objetivo de beneficio
    imprimir_tabla_capacidades(pedidos_json, cap_vol, cap_peso)

def menu_principal():
    """Cada opcion es una llamada a funcion pura."""
    print(f"\n{'-' * 50}")
    print(" UAH-ROUTE — MENU PRINCIPAL \n")
    print("  1. Escenario Basico (Campus UAH)")
    print("  2. Escenario Capacidad Critica")
    print("  3. Escenario Ruteo Complejo")
    print("  4. Escenario Poda (trampa CIE)")
    print("  5. Escenario Libre (Black Friday UAH)")
    print("  6. Generar Escenario Aleatorio")
    print("  0. Salir")
    print(f"{'-' * 50}")

def main():
    """Bucle de eventos principal de la aplicacion."""
    while True:
        menu_principal()
        op = input("Opcion: ").strip()

        if op == "0":
            print("\nSaliendo de UAH-Route.\n")
            break

        elif op in ESCENARIOS:
            datos = cargar_escenario(ESCENARIOS[op])
            if datos:
                ejecutar_escenario(datos)

        elif op == "6":
            try:
                n = int(input("  > Numero de pedidos (ej: 6): "))
            except ValueError:
                n = 6
            print("\n  Generando escenario con recursion...")
            generar_escenario_unico(n)
            datos = cargar_escenario("escenario_generado.json")
            if datos:
                ejecutar_escenario(datos)

        else:
            print("  [!] Opcion no valida.")
            continue

        input("\nPulsa ENTER para volver al menu...")

if __name__ == "__main__":
    main()