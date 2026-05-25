import math


def mostrar_ruta_ascii(ruta, nodos):
    """
    Muestra la secuencia de entregas en una linea de texto con flechas.
    """
    print("\n  ORDEN DE ENTREGA:")
    partes = []
    for id_nodo in ruta:
        nombre = nodos[id_nodo] if nodos and id_nodo < len(nodos) else str(id_nodo)
        partes.append(nombre)
    print("  " + " -> ".join(partes))


def mostrar_carga_lifo(paquetes_lifo):
    """
    Muestra el orden de carga en la furgoneta siguiendo la logica LIFO.
    El primer elemento de la lista es el que va al fondo (ultimo en entregarse).
    El ultimo es el que queda junto a la puerta (primero en entregarse).
    """
    print("\n  ORDEN DE CARGA EN ALMACEN (LIFO):")
    print("  [--- FONDO ---]")
    for i, p in enumerate(paquetes_lifo):
        print(f"    {i + 1}. ID {p.get('id', '?')} -> {p.get('destino', '?')}")
    print("  [--- PUERTA ---]")
    print("  (El paquete junto a la puerta se entrega primero)")


def mostrar_matriz_distancias(grafo, nodos):
    """
    Imprime la matriz de adyacencia del grafo con distancias en metros.
    Solo muestra la distancia (primer elemento de cada arista).
    """
    n = len(grafo)
    ancho = 7
    print("\n  MATRIZ DE DISTANCIAS (metros):")
    cabecera = f"{'':>{ancho}}" + "".join(
        f"{(nodos[j] if nodos else str(j)):>{ancho}}" for j in range(n)
    )
    print("  " + cabecera)
    for i in range(n):
        nombre_i = nodos[i] if nodos else str(i)
        fila = f"{nombre_i:>{ancho}}"
        for j in range(n):
            arista = grafo[i][j]
            if arista == 0 or arista == [0, 0]:
                valor = 0
            elif isinstance(arista, (list, tuple)):
                valor = arista[0]
            else:
                valor = int(arista)
            fila += f"{valor:>{ancho}}"
        print("  " + fila)


def mostrar_grafo_ascii(grafo, nodos):
    """
    Representa el grafo como lista de aristas con distancia y tiempo.
    """
    n = len(grafo)
    print("\n  ARISTAS DEL GRAFO (solo conexiones directas):")
    print(f"  {'Origen':<10} {'Destino':<10} {'Dist(m)':>8} {'Tiempo(min)':>12}")
    print(f"  {'-'*10} {'-'*10} {'-'*8} {'-'*12}")
    for i in range(n):
        for j in range(i + 1, n):
            arista = grafo[i][j]
            if arista == 0 or arista == [0, 0]:
                continue
            if isinstance(arista, (list, tuple)) and len(arista) >= 2:
                if arista[0] == math.inf:
                    continue
                dist_m  = arista[0]
                tiempo  = arista[1]
            elif isinstance(arista, (int, float)) and arista != math.inf:
                dist_m  = arista
                tiempo  = round(arista / 84, 1)
            else:
                continue
            ni = nodos[i] if nodos else str(i)
            nj = nodos[j] if nodos else str(j)
            print(f"  {ni:<10} {nj:<10} {dist_m:>8} {tiempo:>12}")