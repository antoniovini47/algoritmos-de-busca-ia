"""
Visualização de métricas de desempenho dos algoritmos.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_metrics_dataframe(results):
    """
    Cria um DataFrame pandas com as métricas dos algoritmos.
    
    Args:
        results: Dicionário com os resultados dos algoritmos.
        
    Returns:
        DataFrame pandas.
    """
    metrics = []
    
    for algorithm, result in results.items():
        if not result["path"]:  # Ignora algoritmos que não encontraram caminho
            continue
            
        metrics.append({
            "Algoritmo": algorithm,
            "Distância": result["distance"],
            "Nós Expandidos": result["nodes_expanded"],
            "Nós Gerados": result["nodes_generated"],
            "Tamanho Máximo da Fronteira": result["max_frontier_size"],
            "Tempo de Execução (ms)": result["execution_time"]
        })
    
    return pd.DataFrame(metrics)

def plot_metrics_comparison(df, figsize=(14, 10)):
    """
    Plota gráficos comparativos das métricas dos algoritmos.
    
    Args:
        df: DataFrame pandas com as métricas.
        figsize: Tamanho da figura.
        
    Returns:
        fig: Figura matplotlib.
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Configura o estilo
    sns.set_style("whitegrid")
    
    # Gráfico de barras para nós expandidos
    sns.barplot(x="Algoritmo", y="Nós Expandidos", data=df, ax=axes[0, 0], palette="viridis")
    axes[0, 0].set_title("Nós Expandidos por Algoritmo")
    axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=45, ha="right")
    
    # Gráfico de barras para nós gerados
    sns.barplot(x="Algoritmo", y="Nós Gerados", data=df, ax=axes[0, 1], palette="viridis")
    axes[0, 1].set_title("Nós Gerados por Algoritmo")
    axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45, ha="right")
    
    # Gráfico de barras para tamanho máximo da fronteira
    sns.barplot(x="Algoritmo", y="Tamanho Máximo da Fronteira", data=df, ax=axes[1, 0], palette="viridis")
    axes[1, 0].set_title("Tamanho Máximo da Fronteira por Algoritmo")
    axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=45, ha="right")
    
    # Gráfico de barras para tempo de execução
    sns.barplot(x="Algoritmo", y="Tempo de Execução (ms)", data=df, ax=axes[1, 1], palette="viridis")
    axes[1, 1].set_title("Tempo de Execução por Algoritmo (ms)")
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45, ha="right")
    
    plt.tight_layout()
    return fig

def create_metrics_table(df):
    """
    Cria uma tabela formatada com as métricas dos algoritmos.
    
    Args:
        df: DataFrame pandas com as métricas.
        
    Returns:
        Tabela formatada como string.
    """
    # Formata o DataFrame para exibição
    formatted_df = df.copy()
    formatted_df["Distância"] = formatted_df["Distância"].map(lambda x: f"{x:.1f} km")
    formatted_df["Tempo de Execução (ms)"] = formatted_df["Tempo de Execução (ms)"].map(lambda x: f"{x:.2f} ms")
    
    return formatted_df.to_string(index=False)