import heapq
import math
from collections import deque

def heuristic(node, goal):

    return math.sqrt((goal.getX()-node.getX())**2+(goal.getY()-node.getY())**2)

def astar(graph, start, goal):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, (0, start))
    g_scores = {start: 0}
    parents = {}

    while open_list:
        current_cost, current_node = heapq.heappop(open_list)

        if current_node == goal:
            path = []
            while current_node in parents:
                path.append(current_node)
                current_node = parents[current_node]
            path.append(start)
            path.reverse()
            return path

        closed_list.add(current_node)

        for neighbor in graph.getNeighbors(current_node):
            g_score = g_scores[current_node] + 1
            if neighbor not in g_scores or g_score < g_scores[neighbor]:
                g_scores[neighbor] = g_score
                f_score = g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score, neighbor))
                parents[neighbor] = current_node

    return None

def buscar_nodo_en_grafoBFS(grafo, nodo_inicio, nodo_objetivo):
    visitados = set()
    cola = deque([(nodo_inicio, [])])

    while cola:
        nodo, camino = cola.popleft()
        if nodo == nodo_objetivo:
            return camino + [nodo]

        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in grafo.grafoDiccionario[nodo]:
                cola.append((vecino, camino + [nodo]))
    return None

def bidirectional_search(graph, start, goal):
    # Inicialización
    open_list_start = [start]
    open_list_goal = [goal]
    closed_list_start = set()
    closed_list_goal = set()
    parents_start = {start: None}
    parents_goal = {goal: None}

    while open_list_start and open_list_goal:
        # Expandir desde el nodo de inicio
        current_node_start = open_list_start.pop(0)

        if current_node_start in closed_list_goal:
            # Se ha encontrado una intersección, reconstruir el camino
            path = []
            while current_node_start is not None:
                path.append(current_node_start)
                current_node_start = parents_start[current_node_start]
            path.reverse()

            current_node_goal = closed_list_goal.intersection(path).pop()
            while current_node_goal is not None:
                path.append(current_node_goal)
                current_node_goal = parents_goal[current_node_goal]

            return path

        closed_list_start.add(current_node_start)

        # Explorar vecinos desde el nodo de inicio

        for neighbor in graph.getNeighbors(current_node_start):
            if neighbor not in closed_list_start:
                open_list_start.append(neighbor)
                parents_start[neighbor] = current_node_start

        # Expandir desde el nodo objetivo
        current_node_goal = open_list_goal.pop(0)

        if current_node_goal in closed_list_start:
            # Se ha encontrado una intersección, reconstruir el camino
            path = []
            while current_node_goal is not None:
                path.append(current_node_goal)
                current_node_goal = parents_goal[current_node_goal]
            path.reverse()

            current_node_start = closed_list_start.intersection(path).pop()
            while current_node_start is not None:
                path.append(current_node_start)
                current_node_start = parents_start[current_node_start]

            return path

        closed_list_goal.add(current_node_goal)
        # Explorar vecinos desde el nodo objetivo
        for neighbor in graph.getNeighbors(current_node_goal):
            if neighbor not in closed_list_goal:
                open_list_goal.append(neighbor)
                parents_goal[neighbor] = current_node_goal

    # No se ha encontrado un camino
    return None


