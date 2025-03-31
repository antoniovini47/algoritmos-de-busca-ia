"""
Implementação de algoritmos de busca informados.
"""
import time
import heapq
from algorithms.uninformed import Node

def get_heuristic(state, goal, heuristic_data):
    """
    Retorna o valor heurístico para um estado.
    
    Args:
        state: Estado atual.
        goal: Estado objetivo.
        heuristic_data: Dicionário com valores heurísticos pré-calculados.
        
    Returns:
        Valor heurístico.
    """
    if goal == "Bucharest" and state in heuristic_data:
        return heuristic_data[state]
    return 0

def greedy_search(graph, start, goal, heuristic_data):
    """
    Implementação do algoritmo de Busca Gulosa.
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        heuristic_data: Dicionário com valores heurísticos pré-calculados.
        
    Returns:
        Dicionário com os resultados da busca.
    """
    start_time = time.time()
    
    # Métricas
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    
    # Caso especial: início é o objetivo
    if start == goal:
        end_time = time.time()
        return {
            "algorithm": "greedy",
            "path": [start],
            "distance": 0,
            "nodes_expanded": nodes_expanded,
            "nodes_generated": nodes_generated,
            "max_frontier_size": max_frontier_size,
            "execution_time": (end_time - start_time) * 1000,
            "steps": []
        }
    
    # Inicialização
    start_node = Node(state=start)
    frontier = [(get_heuristic(start, goal, heuristic_data), start_node)]  # Fila de prioridade (heurística, nó)
    frontier_states = {start}
    explored = set()
    steps = []
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Registra o estado atual para visualização
        steps.append({
            "frontier": [node.state for _, node in frontier],
            "explored": list(explored),
            "current": None
        })
        
        _, node = heapq.heappop(frontier)
        frontier_states.remove(node.state)
        nodes_expanded += 1
        
        # Registra o nó atual para visualização
        steps[-1]["current"] = node.state
        
        if node.state == goal:
            path = node.path()
            end_time = time.time()
            return {
                "algorithm": "greedy",
                "path": path,
                "distance": node.path_cost,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": steps
            }
        
        explored.add(node.state)
        
        for child in node.expand(graph):
            nodes_generated += 1
            if child.state not in explored and child.state not in frontier_states:
                heapq.heappush(frontier, (get_heuristic(child.state, goal, heuristic_data), child))
                frontier_states.add(child.state)
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "greedy",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": steps
    }

def a_star_search(graph, start, goal, heuristic_data):
    """
    Implementação do algoritmo A*.
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        heuristic_data: Dicionário com valores heurísticos pré-calculados.
        
    Returns:
        Dicionário com os resultados da busca.
    """
    start_time = time.time()
    
    # Métricas
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    
    # Caso especial: início é o objetivo
    if start == goal:
        end_time = time.time()
        return {
            "algorithm": "astar",
            "path": [start],
            "distance": 0,
            "nodes_expanded": nodes_expanded,
            "nodes_generated": nodes_generated,
            "max_frontier_size": max_frontier_size,
            "execution_time": (end_time - start_time) * 1000,
            "steps": []
        }
    
    # Inicialização
    start_node = Node(state=start)
    # Fila de prioridade (f(n) = g(n) + h(n), nó)
    frontier = [(start_node.path_cost + get_heuristic(start, goal, heuristic_data), id(start_node), start_node)]
    frontier_states = {start: start_node.path_cost}
    explored = set()
    steps = []
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Registra o estado atual para visualização
        steps.append({
            "frontier": [node.state for _, _, node in frontier],
            "explored": list(explored),
            "current": None
        })
        
        _, _, node = heapq.heappop(frontier)
        del frontier_states[node.state]
        nodes_expanded += 1
        
        # Registra o nó atual para visualização
        steps[-1]["current"] = node.state
        
        if node.state == goal:
            path = node.path()
            end_time = time.time()
            return {
                "algorithm": "astar",
                "path": path,
                "distance": node.path_cost,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": steps
            }
        
        explored.add(node.state)
        
        for child in node.expand(graph):
            nodes_generated += 1
            if child.state not in explored:
                f_value = child.path_cost + get_heuristic(child.state, goal, heuristic_data)
                
                if child.state not in frontier_states:
                    heapq.heappush(frontier, (f_value, id(child), child))
                    frontier_states[child.state] = child.path_cost
                elif child.state in frontier_states and child.path_cost < frontier_states[child.state]:
                    # Encontra e remove o nó antigo da fronteira
                    for i, (_, _, frontier_node) in enumerate(frontier):
                        if frontier_node.state == child.state:
                            frontier[i] = (f_value, id(child), child)
                            heapq.heapify(frontier)
                            frontier_states[child.state] = child.path_cost
                            break
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "astar",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": steps
    }