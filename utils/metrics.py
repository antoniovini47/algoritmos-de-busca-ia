"""
Funções para cálculo de métricas de desempenho dos algoritmos de busca.
"""
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_path_length(path):
    """
    Calcula o comprimento do caminho em termos do número de nós.
    
    Args:
        path: Lista de nós no caminho.
        
    Returns:
        Comprimento do caminho.
    """
    return len(path) if path else 0

def calculate_path_cost(path, graph):
    """
    Calcula o custo total do caminho.
    
    Args:
        path: Lista de nós no caminho.
        graph: Dicionário representando o grafo.
        
    Returns:
        Custo total do caminho.
    """
    if not path or len(path) < 2:
        return 0
    
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i+1]]
    
    return cost

def format_time(time_ms):
    """
    Formata o tempo em milissegundos para uma string legível.
    
    Args:
        time_ms: Tempo em milissegundos.
        
    Returns:
        String formatada.
    """
    if time_ms < 1:
        return f"{time_ms * 1000:.2f} µs"
    elif time_ms < 1000:
        return f"{time_ms:.2f} ms"
    else:
        return f"{time_ms / 1000:.2f} s"

def create_comparison_table(results):
    """
    Cria uma tabela comparativa dos resultados dos algoritmos.
    
    Args:
        results: Dicionário com os resultados dos algoritmos.
        
    Returns:
        DataFrame pandas.
    """
    data = []
    
    for algorithm, result in results.items():
        if result["path"]:  # Ignora algoritmos que não encontraram caminho
            data.append({
                "Algoritmo": algorithm,
                "Caminho": " → ".join(result["path"]),
                "Distância (km)": result["distance"],
                "Nós Expandidos": result["nodes_expanded"],
                "Nós Gerados": result["nodes_generated"],
                "Máx. Fronteira": result["max_frontier_size"],
                "Tempo (ms)": result["execution_time"]
            })
    
    return pd.DataFrame(data)

def plot_comparison_charts(results, save_path=None):
    """
    Plota gráficos comparativos dos resultados dos algoritmos.
    
    Args:
        results: Dicionário com os resultados dos algoritmos.
        save_path: Caminho para salvar o gráfico (opcional).
        
    Returns:
        Figura matplotlib.
    """
    # Cria DataFrame
    df = pd.DataFrame([
        {
            "Algoritmo": alg,
            "Distância (km)": res["distance"],
            "Nós Expandidos": res["nodes_expanded"],
            "Nós Gerados": res["nodes_generated"],
            "Máx. Fronteira": res["max_frontier_size"],
            "Tempo (ms)": res["execution_time"]
        }
        for alg, res in results.items() if res["path"]
    ])
    
    # Configura o estilo
    sns.set_style("whitegrid")
    
    # Cria subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Gráfico de barras para nós expandidos
    sns.barplot(x="Algoritmo", y="Nós Expandidos", data=df, ax=axes[0, 0], palette="viridis")
    axes[0, 0].set_title("Nós Expandidos por Algoritmo")
    axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=45, ha="right")
    
    # Gráfico de barras para nós gerados
    sns.barplot(x="Algoritmo", y="Nós Gerados", data=df, ax=axes[0, 1], palette="viridis")
    axes[0, 1].set_title("Nós Gerados por Algoritmo")
    axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45, ha="right")
    
    # Gráfico de barras para tamanho máximo da fronteira
    sns.barplot(x="Algoritmo", y="Máx. Fronteira", data=df, ax=axes[1, 0], palette="viridis")
    axes[1, 0].set_title("Tamanho Máximo da Fronteira por Algoritmo")
    axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=45, ha="right")
    
    # Gráfico de barras para tempo de execução
    sns.barplot(x="Algoritmo", y="Tempo (ms)", data=df, ax=axes[1, 1], palette="viridis")
    axes[1, 1].set_title("Tempo de Execução por Algoritmo (ms)")
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45, ha="right")
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    
    return fig

def calculate_efficiency_score(result, max_nodes, max_time):
    """
    Calcula uma pontuação de eficiência para um algoritmo.
    
    Args:
        result: Dicionário com os resultados do algoritmo.
        max_nodes: Número máximo de nós expandidos entre todos os algoritmos.
        max_time: Tempo máximo de execução entre todos os algoritmos.
        
    Returns:
        Pontuação de eficiência (0-100).
    """
    if not result["path"]:
        return 0
    
    # Normaliza os valores (menor é melhor)
    nodes_score = 1 - (result["nodes_expanded"] / max_nodes if max_nodes > 0 else 0)
    time_score = 1 - (result["execution_time"] / max_time if max_time > 0 else 0)
    
    # Calcula a pontuação final (50% nós, 50% tempo)
    return (nodes_score * 50 + time_score * 50)

def rank_algorithms(results):
    """
    Classifica os algoritmos com base na eficiência.
    
    Args:
        results: Dicionário com os resultados dos algoritmos.
        
    Returns:
        Lista de tuplas (algoritmo, pontuação) ordenada por pontuação.
    """
    # Encontra os valores máximos para normalização
    max_nodes = max([res["nodes_expanded"] for _, res in results.items() if res["path"]], default=1)
    max_time = max([res["execution_time"] for _, res in results.items() if res["path"]], default=1)
    
    # Calcula as pontuações
    scores = [
        (alg, calculate_efficiency_score(res, max_nodes, max_time))
        for alg, res in results.items() if res["path"]
    ]
    
    # Ordena por pontuação (maior primeiro)
    return sorted(scores, key=lambda x: x[1], reverse=True)