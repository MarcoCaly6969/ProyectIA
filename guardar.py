import osmnx as ox
import networkx as nx
# Cargar el grafo desde un archivo GraphML
graphml_filepath = 'grafo_cocha.graphml'
graph = ox.load_graphml(filepath=graphml_filepath)

# Obtener y mostrar algunos nodos y aristas
print(f"Ejemplo de algunos nodos: {list(graph.nodes)[:5]}")
print(f"Ejemplo de algunos nodos con atributos: {list(graph.nodes(data=True))[:5]}")
print(f"Ejemplo de algunas aristas: {list(graph.edges)[:5]}")
print(f"Ejemplo de algunas aristas con atributos: {list(graph.edges(data=True))[:5]}")

# Verificar si el grafo es dirigido
print(f"El grafo es dirigido: {graph.is_directed()}")

first = True
# Mostrar pesos (longitud de las calles) de algunas aristas
for u, v, data in list(graph.edges(data=True))[:5]:
    if first:
        x = u
        first = False
    peso = data.get('length', 1)  # El peso por defecto es la longitud de la calle
    print(f"Arista desde {u} a {v} con longitud {peso} metros")
    path = nx.dijkstra_path(graph, x, v, weight='length')
    print(path)
##funciona el dijstraxD