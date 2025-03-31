"""
Visualização do mapa da Romênia e caminhos encontrados.
"""
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch

def create_graph_from_data(cities, roads):
    """
    Cria um grafo NetworkX a partir dos dados do mapa.
    
    Args:
        cities: Dicionário com as cidades e suas coordenadas.
        roads: Lista de tuplas (cidade1, cidade2, distância).
        
    Returns:
        Grafo NetworkX.
    """
    G = nx.Graph()
    
    # Adiciona nós com posições
    for city, pos in cities.items():
        G.add_node(city, pos=pos)
    
    # Adiciona arestas com pesos
    for city1, city2, distance in roads:
        G.add_edge(city1, city2, weight=distance)
    
    return G

def plot_map(G, ax=None, figsize=(12, 8), title="Mapa da Romênia"):
    """
    Plota o mapa da Romênia.
    
    Args:
        G: Grafo NetworkX.
        ax: Eixo matplotlib (opcional).
        figsize: Tamanho da figura.
        title: Título do gráfico.
        
    Returns:
        fig, ax: Figura e eixo matplotlib.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure
    
    # Obtém posições dos nós
    pos = nx.get_node_attributes(G, 'pos')
    
    # Plota nós
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', ax=ax)
    
    # Plota arestas
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, ax=ax)
    
    # Plota rótulos dos nós
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    
    # Plota pesos das arestas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)
    
    ax.set_title(title, fontsize=16)
    ax.axis('off')
    
    return fig, ax

def highlight_path(G, path, ax=None, figsize=(12, 8), title="Caminho Encontrado"):
    """
    Destaca um caminho no mapa.
    
    Args:
        G: Grafo NetworkX.
        path: Lista de cidades no caminho.
        ax: Eixo matplotlib (opcional).
        figsize: Tamanho da figura.
        title: Título do gráfico.
        
    Returns:
        fig, ax: Figura e eixo matplotlib.
    """
    fig, ax = plot_map(G, ax, figsize, title)
    
    if not path or len(path) < 2:
        return fig, ax
    
    # Obtém posições dos nós
    pos = nx.get_node_attributes(G, 'pos')
    
    # Cria subgrafo com o caminho
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    path_nodes = path
    
    # Destaca nós do caminho
    nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_size=500, 
                          node_color='lightgreen', ax=ax)
    
    # Destaca nós inicial e final
    nx.draw_networkx_nodes(G, pos, nodelist=[path[0], path[-1]], node_size=600, 
                          node_color='orange', ax=ax)
    
    # Destaca arestas do caminho
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, 
                          edge_color='green', ax=ax)
    
    return fig, ax

def create_step_by_step_animation(G, steps, algorithm_name, interval=1000):
    """
    Cria uma animação passo a passo da execução do algoritmo.
    
    Args:
        G: Grafo NetworkX.
        steps: Lista de dicionários com informações de cada passo.
        algorithm_name: Nome do algoritmo.
        interval: Intervalo entre frames em milissegundos.
        
    Returns:
        Animação matplotlib.
    """
    if not steps or len(steps) == 0:
        return None
        
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.get_node_attributes(G, 'pos')
    
    def init():
        ax.clear()
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.3, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
        ax.set_title(f"Execução do Algoritmo {algorithm_name}", fontsize=16)
        ax.axis('off')
        return []
    
    def update(frame):
        ax.clear()
        step = steps[frame]
        
        # Plota o grafo base
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.3, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
        
        # Plota nós explorados
        if "explored" in step and step["explored"]:
            nx.draw_networkx_nodes(G, pos, nodelist=step["explored"], 
                                  node_color='lightgray', node_size=400, ax=ax)
        
        # Plota nós na fronteira
        if "frontier" in step and step["frontier"]:
            nx.draw_networkx_nodes(G, pos, nodelist=step["frontier"], 
                                  node_color='lightblue', node_size=400, ax=ax)
        
        # Plota nó atual
        if "current" in step and step["current"]:
            nx.draw_networkx_nodes(G, pos, nodelist=[step["current"]], 
                                  node_color='green', node_size=500, ax=ax)
        
        # Para busca bidirecional
        if "forward_frontier" in step and step["forward_frontier"]:
            nx.draw_networkx_nodes(G, pos, nodelist=step["forward_frontier"], 
                                  node_color='lightblue', node_size=400, ax=ax)
        
        if "backward_frontier" in step and step["backward_frontier"]:
            nx.draw_networkx_nodes(G, pos, nodelist=step["backward_frontier"], 
                                  node_color='lightpink', node_size=400, ax=ax)
        
        if "current_forward" in step and step["current_forward"]:
            nx.draw_networkx_nodes(G, pos, nodelist=[step["current_forward"]], 
                                  node_color='blue', node_size=500, ax=ax)
        
        if "current_backward" in step and step["current_backward"]:
            nx.draw_networkx_nodes(G, pos, nodelist=[step["current_backward"]], 
                                  node_color='red', node_size=500, ax=ax)
        
        # Adiciona informações do passo
        info_text = f"Algoritmo: {algorithm_name}\n"
        info_text += f"Passo: {frame+1}/{len(steps)}\n"
        
        if "depth_limit" in step:
            info_text += f"Limite de profundidade: {step['depth_limit']}\n"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=12,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(f"Execução do Algoritmo {algorithm_name}", fontsize=16)
        ax.axis('off')
        return []
    
    # Cria a animação com função de inicialização
    ani = animation.FuncAnimation(fig, update, frames=len(steps), 
                                 init_func=init, interval=interval, 
                                 blit=False, repeat=True)
    
    # Importante: retorna a animação para que não seja coletada pelo garbage collector
    plt.close(fig)  # Fecha a figura para evitar exibição duplicada
    return ani