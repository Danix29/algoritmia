# src/dp_seleccion.py
# Módulo de selección de pedidos
# Resuelve el problema clásico de la Mochila 0/1 extendido a dos dimensiones restrictivas (peso y volumen).

def seleccionar_pedidos_dp(pedidos, cap_peso, cap_volumen):
    """
    Mochila 0/1 con dos restricciones: peso y volumen.

    Estado teórico: tabla[i][p][v] = maximo beneficio con los i primeros pedidos, capacidad de peso p y capacidad de volumen v disponibles.

    Ecuación de recurrencia:
        Si peso_i > p o vol_i > v:
            tabla[i][p][v] = tabla[i-1][p][v]  (El paquete no cabe, heredamos el óptimo anterior)
        Si no:
            tabla[i][p][v] = max(tabla[i-1][p][v], tabla[i-1][p-peso_i][v-vol_i] + ben_i) (Decisión: ¿Vale más meterlo o dejarlo fuera?)

    Caso base: tabla[0][p][v] = 0 para todo p, v (Con 0 pedidos, el beneficio es 0).
    Complejidad teórica: O(n * P * V) en tiempo y espacio.

    :return: (beneficio_maximo, lista_pedidos_seleccionados)
    """
    n = len(pedidos)
    P = int(cap_peso)
    V = int(cap_volumen)

    # 1. INICIALIZACIÓN (Casos base)
    # Creamos una matriz 3D para evitar la recursión profunda y recalcular subproblemas solapados.
    # Rellenamos de ceros para cumplir el caso base (i=0) directamente.
    tabla = [[[0] * (V + 1) for _ in range(P + 1)] for _ in range(n + 1)]

    # 2. RESOLUCIÓN BOTTOM-UP (Llenado progresivo de la matriz)
    for i in range(1, n + 1):
        pedido = pedidos[i - 1]
        
        # Extracción y prevención de valores nulos mediante .get()
        p_i = int(pedido.get("peso", 0))
        v_i = int(pedido.get("volumen", 1))
        b_i = pedido.get("beneficio", 0)

        for p in range(P + 1):
            for v in range(V + 1):
                # Función de viabilidad: Comprobamos si las capacidades actuales permiten meter el paquete
                if p_i <= p and v_i <= v:
                    # Elegimos la opción que maximiza la ganancia
                    tabla[i][p][v] = max(
                        tabla[i - 1][p][v],
                        tabla[i - 1][p - p_i][v - v_i] + b_i
                    )
                else:
                    # Si excede el peso o volumen disponible en este subproblema, obligatoriamente se descarta
                    tabla[i][p][v] = tabla[i - 1][p][v]

    # 3. TRACEBACK (Reconstrucción de la solución óptima)
    # Recorremos la matriz desde el resultado final hacia atrás para averiguar qué decisiones originaron el máximo.
    seleccionados = []
    p_rest = P
    v_rest = V

    for i in range(n, 0, -1):
        # Si el valor en la etapa actual es diferente al de la etapa anterior (i-1) bajo la misma capacidad,
        # significa inequívocamente que este pedido provocó un incremento de beneficio (fue elegido).
        if tabla[i][p_rest][v_rest] != tabla[i - 1][p_rest][v_rest]:
            pedido_actual = pedidos[i - 1]
            seleccionados.append(pedido_actual)
            
            # Descontamos el "coste" en peso y volumen que supuso elegir este pedido
            # para movernos a las coordenadas del subproblema anterior correcto.
            p_rest -= int(pedido_actual["peso"])
            v_rest -= int(pedido_actual["volumen"])

    # Retornamos la esquina inferior derecha de la matriz (el óptimo global) y la lista de paquetes elegidos
    return tabla[n][P][V], seleccionados