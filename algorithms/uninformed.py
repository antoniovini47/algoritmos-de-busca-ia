"""
Implementação de algoritmos de busca não informados.
"""
import time
from collections import deque
import heapq

class Node:
    """Nó na árvore de busca."""
    
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth
    
    def __lt__(self, other):
        """Comparação para uso em filas de prioridade."""
        return self.path_cost < other.path_cost
    
    def expand(self, graph):
        """Expande o nó atual, gerando todos os nós filhos."""
        children = []
        for neighbor, distance in graph[self.state].items():
            child = Node(
                state=neighbor,
                parent=self,
                action=f"{self.state} to {neighbor}",
                path_cost=self.path_cost + distance,
                depth=self.depth + 1
            )
            children.append(child)
        return children
    
    def path(self):
        """Retorna o caminho do nó inicial até este nó."""
        node, path_back = self, []
        while node:
            path_back.append(node.state)
            node = node.parent
        return list(reversed(path_back))
    
    def path_cost(self):
        """Retorna o custo do caminho do nó inicial até este nó."""
        return self.path_cost

def breadth_first_search(graph, start, goal):
    """
    Implementação do algoritmo de Busca em Largura (BFS).
    
    Args:
        graph: Dicionário representando o grafo, onde as chaves são os nós e os valores
               são dicionários com os vizinhos e seus custos.
        start: Nó inicial.
        goal: Nó objetivo.
        
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
            "algorithm": "bfs",
            "path": [start],
            "distance": 0,
            "nodes_expanded": nodes_expanded,
            "nodes_generated": nodes_generated,
            "max_frontier_size": max_frontier_size,
            "execution_time": (end_time - start_time) * 1000,  # ms
            "steps": []  # Para visualização passo a passo
        }
    
    # Inicialização
    start_node = Node(state=start)
    frontier = deque([start_node])  # Fila FIFO
    explored = set()
    steps = []  # Para visualização passo a passo
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Registra o estado atual para visualização
        steps.append({
            "frontier": [node.state for node in frontier],
            "explored": list(explored),
            "current": None
        })
        
        node = frontier.popleft()
        nodes_expanded += 1
        
        # Registra o nó atual para visualização
        steps[-1]["current"] = node.state
        
        if node.state == goal:
            path = node.path()
            end_time = time.time()
            return {
                "algorithm": "bfs",
                "path": path,
                "distance": node.path_cost,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,  # ms
                "steps": steps
            }
        
        explored.add(node.state)
        
        for child in node.expand(graph):
            nodes_generated += 1
            if child.state not in explored and child.state not in [n.state for n in frontier]:
                frontier.append(child)
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "bfs",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,  # ms
        "steps": steps
    }

def uniform_cost_search(graph, start, goal):
    """
    Implementação do algoritmo de Busca de Custo Uniforme (UCS).
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        
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
            "algorithm": "ucs",
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
    frontier = [(0, start_node)]  # Fila de prioridade (custo, nó)
    frontier_states = {start}  # Conjunto para verificação rápida
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
                "algorithm": "ucs",
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
                heapq.heappush(frontier, (child.path_cost, child))
                frontier_states.add(child.state)
            elif child.state in frontier_states:
                # Encontra o nó na fronteira e atualiza se o novo caminho for melhor
                for i, (cost, frontier_node) in enumerate(frontier):
                    if frontier_node.state == child.state and child.path_cost < cost:
                        frontier[i] = (child.path_cost, child)
                        heapq.heapify(frontier)
                        break
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "ucs",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": steps
    }

def depth_first_search(graph, start, goal):
    """
    Implementação do algoritmo de Busca em Profundidade (DFS).
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        
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
            "algorithm": "dfs",
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
    frontier = [start_node]  # Pilha LIFO
    frontier_states = {start}
    explored = set()
    steps = []
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Registra o estado atual para visualização
        steps.append({
            "frontier": [node.state for node in frontier],
            "explored": list(explored),
            "current": None
        })
        
        node = frontier.pop()
        frontier_states.remove(node.state)
        nodes_expanded += 1
        
        # Registra o nó atual para visualização
        steps[-1]["current"] = node.state
        
        if node.state == goal:
            path = node.path()
            end_time = time.time()
            return {
                "algorithm": "dfs",
                "path": path,
                "distance": node.path_cost,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": steps
            }
        
        explored.add(node.state)
        
        # Expande em ordem reversa para manter a ordem de exploração consistente
        children = node.expand(graph)
        children.reverse()
        
        for child in children:
            nodes_generated += 1
            if child.state not in explored and child.state not in frontier_states:
                frontier.append(child)
                frontier_states.add(child.state)
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "dfs",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": steps
    }

def depth_limited_search(graph, start, goal, depth_limit=10):
    """
    Implementação do algoritmo de Busca em Profundidade Limitada (DLS).
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        depth_limit: Limite de profundidade da busca.
        
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
            "algorithm": "dls",
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
    frontier = [start_node]  # Pilha LIFO
    frontier_states = {start}
    explored = set()
    steps = []
    
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        
        # Registra o estado atual para visualização
        steps.append({
            "frontier": [node.state for node in frontier],
            "explored": list(explored),
            "current": None
        })
        
        node = frontier.pop()
        frontier_states.remove(node.state)
        nodes_expanded += 1
        
        # Registra o nó atual para visualização
        steps[-1]["current"] = node.state
        
        if node.state == goal:
            path = node.path()
            end_time = time.time()
            return {
                "algorithm": "dls",
                "path": path,
                "distance": node.path_cost,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": steps
            }
        
        explored.add(node.state)
        
        # Só expande se não atingiu o limite de profundidade
        if node.depth < depth_limit:
            # Expande em ordem reversa para manter a ordem de exploração consistente
            children = node.expand(graph)
            children.reverse()
            
            for child in children:
                nodes_generated += 1
                if child.state not in explored and child.state not in frontier_states:
                    frontier.append(child)
                    frontier_states.add(child.state)
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "dls",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": steps
    }

def iterative_deepening_search(graph, start, goal, max_depth=100):
    """
    Implementação do algoritmo de Busca de Aprofundamento Iterativo (IDS).
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        max_depth: Profundidade máxima a ser considerada.
        
    Returns:
        Dicionário com os resultados da busca.
    """
    start_time = time.time()
    
    # Métricas acumuladas
    total_nodes_expanded = 0
    total_nodes_generated = 0
    max_frontier_size = 0
    all_steps = []
    
    # Caso especial: início é o objetivo
    if start == goal:
        end_time = time.time()
        return {
            "algorithm": "ids",
            "path": [start],
            "distance": 0,
            "nodes_expanded": 1,
            "nodes_generated": 1,
            "max_frontier_size": 1,
            "execution_time": (end_time - start_time) * 1000,
            "steps": []
        }
    
    for depth in range(max_depth):
        # Executa DLS com o limite de profundidade atual
        result = depth_limited_search(graph, start, goal, depth)
        
        # Acumula métricas
        total_nodes_expanded += result["nodes_expanded"]
        total_nodes_generated += result["nodes_generated"]
        max_frontier_size = max(max_frontier_size, result["max_frontier_size"])
        
        # Adiciona os passos desta iteração
        for step in result["steps"]:
            step["depth_limit"] = depth
            all_steps.append(step)
        
        # Se encontrou um caminho, retorna o resultado
        if result["path"]:
            end_time = time.time()
            return {
                "algorithm": "ids",
                "path": result["path"],
                "distance": result["distance"],
                "nodes_expanded": total_nodes_expanded,
                "nodes_generated": total_nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": all_steps
            }
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "ids",
        "path": [],
        "distance": 0,
        "nodes_expanded": total_nodes_expanded,
        "nodes_generated": total_nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": all_steps
    }

def bidirectional_search(graph, start, goal):
    """
    Implementação do algoritmo de Busca Bidirecional.
    
    Args:
        graph: Dicionário representando o grafo.
        start: Nó inicial.
        goal: Nó objetivo.
        
    Returns:
        Dicionário com os resultados da busca.
    """
    start_time = time.time()
    
    # Métricas
    nodes_expanded = 0
    nodes_generated = 2  # Nós iniciais de ambas as direções
    max_frontier_size = 2
    
    # Caso especial: início é o objetivo
    if start == goal:
        end_time = time.time()
        return {
            "algorithm": "bidirectional",
            "path": [start],
            "distance": 0,
            "nodes_expanded": nodes_expanded,
            "nodes_generated": nodes_generated,
            "max_frontier_size": max_frontier_size,
            "execution_time": (end_time - start_time) * 1000,
            "steps": []
        }
    
    # Inicialização da busca para frente
    start_node = Node(state=start)
    forward_frontier = deque([start_node])
    forward_explored = {}  # Dicionário para armazenar nós explorados
    
    # Inicialização da busca para trás
    goal_node = Node(state=goal)
    backward_frontier = deque([goal_node])
    backward_explored = {}  # Dicionário para armazenar nós explorados
    
    steps = []
    
    # Cria grafo reverso para a busca para trás
    reverse_graph = {}
    for city in graph:
        reverse_graph[city] = {}
    for city, neighbors in graph.items():
        for neighbor, distance in neighbors.items():
            reverse_graph[neighbor][city] = distance
    
    while forward_frontier and backward_frontier:
        max_frontier_size = max(max_frontier_size, len(forward_frontier) + len(backward_frontier))
        
        # Registra o estado atual para visualização
        steps.append({
            "forward_frontier": [node.state for node in forward_frontier],
            "backward_frontier": [node.state for node in backward_frontier],
            "forward_explored": list(forward_explored.keys()),
            "backward_explored": list(backward_explored.keys()),
            "current_forward": None,
            "current_backward": None
        })
        
        # Busca para frente
        forward_node = forward_frontier.popleft()
        nodes_expanded += 1
        steps[-1]["current_forward"] = forward_node.state
        
        forward_explored[forward_node.state] = forward_node
        
        # Verifica se encontrou um nó em comum
        if forward_node.state in backward_explored:
            backward_node = backward_explored[forward_node.state]
            
            # Constrói o caminho completo
            forward_path = forward_node.path()
            backward_path = backward_node.path()
            backward_path.reverse()
            
            # Remove a duplicação do nó de encontro
            backward_path.pop(0)
            
            path = forward_path + backward_path
            distance = forward_node.path_cost + backward_node.path_cost
            
            end_time = time.time()
            return {
                "algorithm": "bidirectional",
                "path": path,
                "distance": distance,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": steps
            }
        
        # Expande nós da busca para frente
        for child in forward_node.expand(graph):
            nodes_generated += 1
            if child.state not in forward_explored and child.state not in [n.state for n in forward_frontier]:
                forward_frontier.append(child)
        
        # Busca para trás
        backward_node = backward_frontier.popleft()
        nodes_expanded += 1
        steps[-1]["current_backward"] = backward_node.state
        
        backward_explored[backward_node.state] = backward_node
        
        # Verifica se encontrou um nó em comum
        if backward_node.state in forward_explored:
            forward_node = forward_explored[backward_node.state]
            
            # Constrói o caminho completo
            forward_path = forward_node.path()
            backward_path = backward_node.path()
            backward_path.reverse()
            
            # Remove a duplicação do nó de encontro
            backward_path.pop(0)
            
            path = forward_path + backward_path
            distance = forward_node.path_cost + backward_node.path_cost
            
            end_time = time.time()
            return {
                "algorithm": "bidirectional",
                "path": path,
                "distance": distance,
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "execution_time": (end_time - start_time) * 1000,
                "steps": steps
            }
        
        # Expande nós da busca para trás
        for child in backward_node.expand(reverse_graph):
            nodes_generated += 1
            if child.state not in backward_explored and child.state not in [n.state for n in backward_frontier]:
                backward_frontier.append(child)
    
    # Nenhum caminho encontrado
    end_time = time.time()
    return {
        "algorithm": "bidirectional",
        "path": [],
        "distance": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": 0,
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "execution_time": (end_time - start_time) * 1000,
        "steps": steps
    }