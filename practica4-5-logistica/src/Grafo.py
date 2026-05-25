import json
import networkx as nx
import matplotlib.pyplot as plt

# 1. Cargar los datos desde el archivo JSON
with open('topologia_uah.json', 'r') as archivo:
    datos = json.load(archivo)

# 2. Inicializar el grafo
G = nx.Graph()
posiciones = {}

# 3. Procesar nodos y coordenadas
for nodo in datos['nodos']:
    G.add_node(nodo['id'])
    # Guardamos las coordenadas X e Y en un diccionario para el mapeo espacial
    posiciones[nodo['id']] = (nodo['x'], nodo['y'])

# 4. Procesar aristas y pesos (distancia y tiempo)
for arista in datos['caminos']:
    G.add_edge(
        arista['origen'], 
        arista['destino'], 
        peso=arista['distancia_m'], 
        tiempo=arista['tiempo_min']
    )

# 5. Configurar el lienzo y renderizar la imagen
plt.figure(figsize=(12, 10))

# Dibujar nodos y conexiones
nx.draw(
    G, posiciones, 
    with_labels=True, 
    node_color="#2c3e50", 
    node_size=1000, 
    font_color="white",
    font_size=9, 
    font_weight="bold", 
    edge_color="#bdc3c7", 
    width=2.5
)

# Extraer y formatear las etiquetas para las líneas (mostrará metros y minutos)
etiquetas_aristas = {
    (u, v): f"{d['peso']}m\n{d['tiempo']} min" 
    for u, v, d in G.edges(data=True)
}

nx.draw_networkx_edge_labels(
    G, posiciones,
    edge_labels=etiquetas_aristas,
    font_size=9,
    font_color="#e74c3c",
    font_weight="bold",
    label_pos=0.5
)

plt.title("Visualización del Grafo: Campus UAH (Lectura desde JSON)", fontsize=14, pad=20)
plt.grid(True, linestyle='--', alpha=0.3)

# La función show() es la que compila el canvas y despliega la imagen en pantalla
plt.show()