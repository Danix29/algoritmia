<img src="https://capsule-render.vercel.app/api?type=waving&color=3776AB&height=160&section=header&text=algoritmia&fontSize=34&fontColor=FFFFFF&fontAlignY=40&desc=Algoritmia%20y%20Complejidad%20%7C%20UAH%202025-26&descAlignY=60&descColor=9FE1CB" width="100%"/>

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Algorithms](https://img.shields.io/badge/Algorithms-1D9E75?style=for-the-badge)
![Complexity](https://img.shields.io/badge/Complexity-085041?style=for-the-badge)
![UAH](https://img.shields.io/badge/UAH-GII-085041?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-1D9E75?style=for-the-badge)

</div>

---

## About

**Asignatura:** Algoritmia y Complejidad &middot; UAH GII &middot; Curso 2025-26

Design, analysis and implementation of advanced algorithms. Theoretical complexity analysis combined with empirical performance measurement across multiple algorithmic paradigms.

---

## Topics covered

| Paradigm | Algorithms | Complexity |
|----------|-----------|------------|
| Divide and Conquer | Mergesort, Quicksort, binary search | O(n log n) |
| Dynamic Programming | Knapsack 0/1, LCS, matrix chain | O(n&middot;W), O(n&sup2;) |
| Backtracking | TSP, N-Queens, graph coloring | O(n!) worst case |
| Branch and Bound | TSP optimized, job scheduling | Subexponential in practice |
| Greedy | Kruskal, Prim, Dijkstra, Huffman | O(E log V) |
| Graph algorithms | Floyd-Warshall, Bellman-Ford, topological sort | O(V&sup3;), O(VE) |

---

## Practices

| # | Name | Description |
|---|------|-------------|
| P4-5 | [logistica-urbana](./practica4-5-logistica/) | Two-module system: Knapsack 0/1 with DP O(n&middot;C) + TSP with Backtracking and Branch and Bound pruning. Greedy vs DP comparison. Floyd-Warshall precalculation. 5 test scenarios in JSON |

---

## Project structure

```
algoritmia/
└── practica4-5-logistica/
    ├── README.md
    ├── Informe_Practica_AyC.pdf
    └── src/
        ├── main.py                    # Entry point and interactive menu
        ├── dp_seleccion.py            # Knapsack 0/1 module (weight + volume)
        ├── backtracking_ruta.py       # TSP Backtracking + B&B + Floyd-Warshall
        ├── Grafo.py                   # Graph visualization
        ├── topologia_uah.json         # UAH campus graph (nodes and edges)
        ├── mejoras/
        │   ├── comparador_voraz.py    # Greedy vs DP comparison
        │   ├── floyd_warshall.py      # All-pairs shortest path
        │   ├── quicksort_pedidos.py   # Multi-criteria Quicksort
        │   └── busqueda_binaria.py    # Binary search on capacity
        ├── utils/
        │   ├── generador_escenarios.py
        │   └── visualizador.py
        ├── data/escenarios/           # 5 JSON test scenarios
        └── tests/
            ├── test_dp.py
            └── test_backtracking.py
```

---

## Complexity summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Knapsack DP | O(n&middot;C) | O(n&middot;C) |
| TSP Backtracking | O(n!) worst | O(n) |
| TSP with pruning | Subexponential in practice | O(n) |
| Floyd-Warshall | O(V&sup3;) | O(V&sup2;) |
| Greedy (comparison) | O(n log n) | O(n) |

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=3776AB&height=100&section=footer" width="100%"/>

*Algoritmia y Complejidad &middot; UAH GII &middot; 2025-26*
</div>
