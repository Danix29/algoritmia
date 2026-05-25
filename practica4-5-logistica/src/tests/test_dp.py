# src/tests/test_dp.py
# Pruebas unitarias para el módulo de Selección de Pedidos mediante programación dinámica.
# Valida la optimalidad de la mochila 0/1 con restricciones bidimensionales (peso y volumen).

import sys
import os
# Configuración del path para importar el módulo dp_seleccion sin requerir instalación de paquetes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dp_seleccion import seleccionar_pedidos_dp


def test_sin_pedidos():
    """
    Caso base / límite: Verifica que el algoritmo maneje correctamente una lista vacía.
    El beneficio debe ser 0 y la lista de seleccionados debe estar vacía.
    """
    ben, eleg = seleccionar_pedidos_dp([], 10, 10)
    assert ben == 0 and eleg == []


def test_capacidad_cero():
    """
    Caso límite: Verifica que con capacidad nula (peso o volumen) no se seleccione ningún pedido, independientemente de su beneficio.
    """
    pedidos = [{"id": 1, "peso": 2, "volumen": 1, "beneficio": 50}]
    ben, eleg = seleccionar_pedidos_dp(pedidos, 0, 0)
    assert ben == 0 and eleg == []


def test_caso_basico():
    """
    Valida el comportamiento esperado con el escenario básico del enunciado.
    Con capacidad de 8kg, debe elegir la combinación óptima de los pedidos 2 y 3 (110€), 
    demostrando que la relación de recurrencia de la DP funciona correctamente.
    """
    pedidos = [
        {"id": 1, "peso": 2, "volumen": 2, "beneficio": 30},
        {"id": 2, "peso": 5, "volumen": 3, "beneficio": 70},
        {"id": 3, "peso": 3, "volumen": 2, "beneficio": 40},
        {"id": 4, "peso": 1, "volumen": 1, "beneficio": 10},
        {"id": 5, "peso": 4, "volumen": 3, "beneficio": 60},
    ]
    ben, eleg = seleccionar_pedidos_dp(pedidos, 8, 10)
    assert ben == 110
    ids = sorted(p["id"] for p in eleg)
    assert ids == [2, 3]


def test_restriccion_volumen_actua():
    """
    Validación de restricción bidimensional: Comprueba que el volumen actúa como un límite real.
    Un pedido con alto beneficio pero exceso de volumen debe ser rechazado en favor de uno 
    que maximice el beneficio dentro de ambas restricciones (peso y volumen).
    """
    pedidos = [
        {"id": 1, "peso": 1, "volumen": 5, "beneficio": 100},
        {"id": 2, "peso": 1, "volumen": 1, "beneficio": 60},
    ]
    ben, eleg = seleccionar_pedidos_dp(pedidos, 10, 2)
    assert ben == 60
    assert eleg[0]["id"] == 2


def test_pedido_trampa_rechazado():
    """
    Prueba de estrategia global: Verifica que la DP no sea voraz. 
    Debe rechazar un pedido individual grande (trampa) si la combinación de varios pedidos pequeños ofrece un beneficio total mayor.
    """
    pedidos = [
        {"id": 1, "peso": 12, "volumen": 8, "beneficio": 20},
        {"id": 2, "peso": 1,  "volumen": 1, "beneficio": 90},
        {"id": 4, "peso": 2,  "volumen": 1, "beneficio": 100},
        {"id": 5, "peso": 3,  "volumen": 2, "beneficio": 60},
    ]
    ben, eleg = seleccionar_pedidos_dp(pedidos, 15, 20)
    ids = [p["id"] for p in eleg]
    assert 1 not in ids # El pedido trampa (ID 1) debe ser ignorado
    assert ben >= 250


def test_uso_completo_de_capacidad():
    """
    Prueba de saturación: Verifica que el algoritmo es capaz de llenar la capacidad 
    al 100% si existen pedidos que sumen exactamente el límite de peso y volumen.
    """
    pedidos = [
        {"id": 1, "peso": 5, "volumen": 3, "beneficio": 50},
        {"id": 2, "peso": 5, "volumen": 3, "beneficio": 50},
    ]
    ben, eleg = seleccionar_pedidos_dp(pedidos, 10, 10)
    assert ben == 100
    assert len(eleg) == 2


if __name__ == "__main__":
    for nombre, func in list(globals().items()):
        if nombre.startswith("test_") and callable(func):
            try:
                func()
                print(f"  OK  {nombre}")
            except AssertionError as e:
                print(f"  FALLO  {nombre}: {e}")