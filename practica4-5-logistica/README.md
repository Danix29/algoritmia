# UAH-Route — Optimizacion Logistica Urbana

**Practica 4-5 — Algoritmia y Complejidad | Curso 2025-26**
Universidad de Alcala, Escuela Politecnica Superior
Grado en Ingenieria Informatica

---

## Descripcion

Sistema de optimizacion logistica para el campus UAH que resuelve dos problemas encadenados:

1. **Seleccion optima de pedidos** — Mochila 0/1 con restriccion de peso y volumen (Programacion Dinamica tridimensional).
2. **Planificacion de ruta de entrega** — TSP sobre el grafo real del campus (Backtracking con Ramificacion y Poda + Floyd-Warshall).

El grafo del campus se carga desde `topologia_uah.json`. Al no ser completo, se precalculan las distancias minimas reales entre todos los pares de edificios con Floyd-Warshall antes de lanzar el backtracking.

---

## Requisitos

- Python 3.10 o superior
- Sin dependencias externas para los algoritmos principales

---

## Ejecucion

```bash
cd src
python main.py
```

### Menu

```
1. Escenario Basico (Campus UAH)
2. Escenario Capacidad Critica
3. Escenario Ruteo Complejo
4. Escenario Poda (trampa CIE)
5. Escenario Libre (Black Friday UAH)
6. Generar Escenario Aleatorio
0. Salir
```

Cada opcion ejecuta el pipeline completo de cinco fases:

| Fase | Descripcion |
|---|---|
| 1 | Carga de datos del vehiculo y pedidos |
| 2 | Seleccion optima por DP + comparacion voraz + ranking Quicksort |
| 3 | Floyd-Warshall + Backtracking con/sin poda (o Held-Karp si n > 10) |
| 4 | Logistica LIFO y visualizacion de ruta |
| 5 | Recalculo dinamico ante incidencia en la red viaria |

---

## Estructura del proyecto

```
src/
├── main.py                        # Punto de entrada y menu interactivo
├── dp_seleccion.py                # Mochila 0/1 DP (peso + volumen) — Tema 4
├── backtracking_ruta.py           # TSP Backtracking + poda + Floyd-Warshall + Held-Karp — Tema 5
├── Grafo.py                       # Visualizacion del grafo UAH con networkx
├── topologia_uah.json             # Grafo real del campus UAH (nodos y aristas)
│
├── mejoras/
│   ├── comparador_voraz.py        # Mejora 3 (T2): Voraz vs DP, gap de calidad
│   ├── floyd_warshall.py          # Mejora 7 (Avanzada): all-pairs shortest path
│   ├── quicksort_pedidos.py       # Mejora 5 (T3): Quicksort multi-criterio D&V
│   └── busqueda_binaria.py        # Mejora 6 (T3): Capacidad minima por objetivo %
│
├── utils/
│   ├── generador_escenarios.py    # Mejora 1 (T1): Generacion recursiva con nodos UAH
│   └── visualizador.py           # Ruta ASCII, LIFO, matriz de distancias
│
├── data/
│   ├── escenarios/                # 5 escenarios fijos + escenario_generado.json
│   └── resultados/                # Directorio para resultados de ejecucion
│
└── tests/
    ├── test_dp.py                 # 6 tests unitarios mochila DP
    └── test_backtracking.py       # 7 tests unitarios backtracking y Floyd-Warshall
```

---

## Tests

```bash
cd src
python tests/test_dp.py
python tests/test_backtracking.py
```

Salida esperada: todos los tests con `OK`.

---

## Algoritmos implementados

| Modulo | Algoritmo | Complejidad |
|---|---|---|
| `dp_seleccion.py` | Mochila 0/1 (peso + volumen) | O(n · P · V) |
| `backtracking_ruta.py` | Floyd-Warshall (preprocesado) | O(V³) |
| `backtracking_ruta.py` | TSP Backtracking con poda | O(n!) peor caso |
| `backtracking_ruta.py` | Held-Karp (activo si n > 10) | O(n² · 2ⁿ) |
| `mejoras/comparador_voraz.py` | Voraz por ratio ben/peso | O(n log n) |
| `mejoras/quicksort_pedidos.py` | Quicksort mediana-de-tres | O(n log n) medio |
| `mejoras/busqueda_binaria.py` | Busqueda binaria sobre C | O(log C · n · P · V) |
| `utils/generador_escenarios.py` | Generacion recursiva | O(n) |

---

## Escenarios de prueba

| # | Nombre | N ped. | C peso | Objetivo |
|---|---|---|---|---|
| 1 | Basico | 5 | 30 kg | Validacion funcional del sistema completo |
| 2 | Capacidad Critica | 9 | 15 kg | Demostrar superioridad de DP sobre voraz |
| 3 | Ruteo Complejo | 5 | 50 kg | TSP con grafo homogeneo (poda 0%) |
| 4 | Poda (trampa CIE) | 5 | 50 kg | Poda activa en grafo heterogeneo (42%) |
| 5 | Libre (Black Friday) | 9 | 20 kg | Caso realista con pedido trampa |
| 6 | Autogenerado | 1-9 | variable | Generacion recursiva con nodos UAH reales |

---

## Notas tecnicas

- **Grafo no completo**: Floyd-Warshall se aplica antes de cada ejecucion del backtracking para calcular las distancias reales entre edificios sin conexion directa.
- **Limite de destinos**: si el numero de nodos a visitar supera 10, el sistema conmuta automaticamente a Held-Karp (O(n² · 2ⁿ)) para evitar tiempos inasumibles.
- **Timeout**: un limite de 5 segundos protege el backtracking en casos extremos.
- **Logistica LIFO**: el backtracking penaliza con +15 unidades de coste las rutas que no respetan el orden de carga.
- **Escenario autogenerado**: usa los nodos reales del campus UAH (hasta 9 edificios de entrega) con distancias extraidas de `topologia_uah.json` via Floyd-Warshall.
