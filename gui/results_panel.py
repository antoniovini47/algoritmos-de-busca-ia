"""
Painel de resultados para a interface gráfica.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTextEdit, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd

class ResultsPanel(QWidget):
    """
    Painel para exibição de resultados dos algoritmos.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurações
        self.current_result = None
        self.results_history = {}
        
        # Configura a interface
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        layout = QVBoxLayout(self)
        
        # Abas para diferentes visualizações
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Aba de texto
        self.text_tab = QWidget()
        text_layout = QVBoxLayout(self.text_tab)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        text_layout.addWidget(self.results_text)
        
        self.tabs.addTab(self.text_tab, "Texto")
        
        # Aba de tabela
        self.table_tab = QWidget()
        table_layout = QVBoxLayout(self.table_tab)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Métrica", "Valor", "", "", "", ""
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.results_table)
        
        self.tabs.addTab(self.table_tab, "Tabela")
        
        # Aba de gráfico
        self.chart_tab = QWidget()
        chart_layout = QVBoxLayout(self.chart_tab)
        
        self.chart_canvas = FigureCanvas(plt.figure(figsize=(5, 4)))
        chart_layout.addWidget(self.chart_canvas)
        
        self.chart_toolbar = NavigationToolbar(self.chart_canvas, self.chart_tab)
        chart_layout.addWidget(self.chart_toolbar)
        
        self.tabs.addTab(self.chart_tab, "Gráfico")
        
        # Aba de comparação
        self.comparison_tab = QWidget()
        comparison_layout = QVBoxLayout(self.comparison_tab)
        
        self.comparison_table = QTableWidget()
        comparison_layout.addWidget(self.comparison_table)
        
        self.comparison_canvas = FigureCanvas(plt.figure(figsize=(5, 4)))
        comparison_layout.addWidget(self.comparison_canvas)
        
        self.comparison_toolbar = NavigationToolbar(self.comparison_canvas, self.comparison_tab)
        comparison_layout.addWidget(self.comparison_toolbar)
        
        self.tabs.addTab(self.comparison_tab, "Comparação")
    
    def update_result(self, result):
        """
        Atualiza o painel com um novo resultado.
        
        Args:
            result: Dicionário com os resultados do algoritmo.
        """
        self.current_result = result
        
        # Armazena o resultado no histórico
        self.results_history[result["algorithm"]] = result
        
        # Atualiza a aba de texto
        self.update_text_tab(result)
        
        # Atualiza a aba de tabela
        self.update_table_tab(result)
        
        # Atualiza a aba de gráfico
        self.update_chart_tab(result)
        
        # Muda para a aba de texto
        self.tabs.setCurrentWidget(self.text_tab)
    
    def update_text_tab(self, result):
        """
        Atualiza a aba de texto com os resultados.
        
        Args:
            result: Dicionário com os resultados do algoritmo.
        """
        algorithm_names = {
            "bfs": "Busca em Largura (BFS)",
            "ucs": "Busca de Custo Uniforme (UCS)",
            "dfs": "Busca em Profundidade (DFS)",
            "dls": "Busca em Profundidade Limitada (DLS)",
            "ids": "Busca de Aprofundamento Iterativo (IDS)",
            "bidirectional": "Busca Bidirecional",
            "greedy": "Busca Gulosa",
            "astar": "Algoritmo A*"
        }
        
        text = f"Algoritmo: {algorithm_names.get(result['algorithm'], result['algorithm'])}\n\n"
        
        if result["path"]:
            text += f"Caminho encontrado: {' → '.join(result['path'])}\n"
            text += f"Distância total: {result['distance']} km\n"
            text += f"Número de cidades no caminho: {len(result['path'])}\n\n"
        else:
            text += "Nenhum caminho encontrado.\n\n"
        
        text += "Métricas de desempenho:\n"
        text += f"Nós expandidos: {result['nodes_expanded']}\n"
        text += f"Nós gerados: {result['nodes_generated']}\n"
        text += f"Tamanho máximo da fronteira: {result['max_frontier_size']}\n"
        text += f"Tempo de execução: {result['execution_time']:.2f} ms\n"
        
        self.results_text.setText(text)
    
    def update_table_tab(self, result):
        """
        Atualiza a aba de tabela com os resultados.
        
        Args:
            result: Dicionário com os resultados do algoritmo.
        """
        self.results_table.setRowCount(0)
        
        if not result["path"]:
            self.results_table.setRowCount(1)
            self.results_table.setItem(0, 0, QTableWidgetItem("Resultado"))
            self.results_table.setItem(0, 1, QTableWidgetItem("Nenhum caminho encontrado"))
            return
        
        # Adiciona as métricas à tabela
        metrics = [
            ("Algoritmo", result["algorithm"]),
            ("Caminho", " → ".join(result["path"])),
            ("Distância", f"{result['distance']} km"),
            ("Nós Expandidos", str(result["nodes_expanded"])),
            ("Nós Gerados", str(result["nodes_generated"])),
            ("Tamanho Máximo da Fronteira", str(result["max_frontier_size"])),
            ("Tempo de Execução", f"{result['execution_time']:.2f} ms")
        ]
        
        self.results_table.setRowCount(len(metrics))
        
        for i, (metric, value) in enumerate(metrics):
            self.results_table.setItem(i, 0, QTableWidgetItem(metric))
            self.results_table.setItem(i, 1, QTableWidgetItem(value))
    
    def update_chart_tab(self, result):
        """
        Atualiza a aba de gráfico com os resultados.
        
        Args:
            result: Dicionário com os resultados do algoritmo.
        """
        if not result["path"]:
            return
        
        # Limpa o gráfico
        self.chart_canvas.figure.clear()
        
        # Cria um gráfico de barras com as métricas
        ax = self.chart_canvas.figure.add_subplot(111)
        
        metrics = {
            "Nós Expandidos": result["nodes_expanded"],
            "Nós Gerados": result["nodes_generated"],
            "Máx. Fronteira": result["max_frontier_size"]
        }
        
        ax.bar(metrics.keys(), metrics.values(), color="skyblue")
        ax.set_title(f"Métricas para {result['algorithm']}")
        ax.set_ylabel("Quantidade")
        
        for i, v in enumerate(metrics.values()):
            ax.text(i, v + 0.1, str(v), ha="center")
        
        self.chart_canvas.figure.tight_layout()
        self.chart_canvas.draw()
    
    def update_comparison(self, results):
        """
        Atualiza a aba de comparação com múltiplos resultados.
        
        Args:
            results: Dicionário com os resultados de vários algoritmos.
        """
        # Limpa a tabela de comparação
        self.comparison_table.clear()
        
        # Cria um DataFrame com os resultados
        data = []
        for alg, res in results.items():
            if res["path"]:
                data.append({
                    "Algoritmo": alg,
                    "Distância (km)": res["distance"],
                    "Nós Expandidos": res["nodes_expanded"],
                    "Nós Gerados": res["nodes_generated"],
                    "Máx. Fronteira": res["max_frontier_size"],
                    "Tempo (ms)": res["execution_time"]
                })
        
        df = pd.DataFrame(data)
        
        # Configura a tabela
        self.comparison_table.setRowCount(len(df))
        self.comparison_table.setColumnCount(len(df.columns))
        self.comparison_table.setHorizontalHeaderLabels(df.columns)
        
        # Preenche a tabela
        for i in range(len(df)):
            for j in range(len(df.columns)):
                value = df.iloc[i, j]
                if isinstance(value, float):
                    item = QTableWidgetItem(f"{value:.2f}")
                else:
                    item = QTableWidgetItem(str(value))
                self.comparison_table.setItem(i, j, item)
        
        self.comparison_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Atualiza o gráfico de comparação
        self.comparison_canvas.figure.clear()
        
        # Cria subplots
        fig = self.comparison_canvas.figure
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)
        
        # Gráfico de barras para nós expandidos
        algorithms = df["Algoritmo"]
        ax1.bar(algorithms, df["Nós Expandidos"], color="skyblue")
        ax1.set_title("Nós Expandidos")
        ax1.set_xticklabels(algorithms, rotation=45, ha="right")
        
        # Gráfico de barras para nós gerados
        ax2.bar(algorithms, df["Nós Gerados"], color="lightgreen")
        ax2.set_title("Nós Gerados")
        ax2.set_xticklabels(algorithms, rotation=45, ha="right")
        
        # Gráfico de barras para tamanho máximo da fronteira
        ax3.bar(algorithms, df["Máx. Fronteira"], color="salmon")
        ax3.set_title("Tamanho Máximo da Fronteira")
        ax3.set_xticklabels(algorithms, rotation=45, ha="right")
        
        # Gráfico de barras para tempo de execução
        ax4.bar(algorithms, df["Tempo (ms)"], color="purple")
        ax4.set_title("Tempo de Execução (ms)")
        ax4.set_xticklabels(algorithms, rotation=45, ha="right")
        
        fig.tight_layout()
        self.comparison_canvas.draw()
        
        # Muda para a aba de comparação
        self.tabs.setCurrentWidget(self.comparison_tab)