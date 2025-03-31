"""
Interface gráfica principal da aplicação.
"""
import sys
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QTabWidget, QTextEdit, QGroupBox, QGridLayout, QSplitter, QFrame)
from PySide6.QtCore import Qt
from data.romania_map import CITIES, ROADS, STRAIGHT_LINE_TO_BUCHAREST
from algorithms.uninformed import (breadth_first_search, uniform_cost_search, 
                                  depth_first_search, depth_limited_search,
                                  iterative_deepening_search, bidirectional_search)
from algorithms.informed import greedy_search, a_star_search
from visualization.map_view import (create_graph_from_data, plot_map, 
                                   highlight_path, create_step_by_step_animation)
from visualization.metrics_view import (create_metrics_dataframe, 
                                       plot_metrics_comparison, create_metrics_table)

class MatplotlibCanvas(FigureCanvas):
    """Canvas para exibir gráficos matplotlib."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout()

class MainWindow(QMainWindow):
    """Janela principal da aplicação."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Explorador de Algoritmos de Busca")
        self.setGeometry(100, 100, 1200, 800)
        
        # Cria o grafo
        self.roads_list = [(city1, city2, distance) for city1, city2, distance in ROADS]
        self.graph = create_graph_from_data(CITIES, self.roads_list)
        
        # Cria o dicionário de adjacência para os algoritmos
        self.adjacency_dict = {}
        for city in CITIES:
            self.adjacency_dict[city] = {}
        
        for city1, city2, distance in self.roads_list:
            self.adjacency_dict[city1][city2] = distance
            self.adjacency_dict[city2][city1] = distance
        
        # Resultados dos algoritmos
        self.results = {}
        
        # Referência para a animação
        self.animation = None
        
        # Configura a interface
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Splitter para dividir controles e visualização
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Painel de controle (esquerda)
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        splitter.addWidget(control_panel)
        
        # Grupo de seleção de cidades
        cities_group = QGroupBox("Seleção de Cidades")
        cities_layout = QGridLayout()
        cities_group.setLayout(cities_layout)
        
        # Cidade de origem
        cities_layout.addWidget(QLabel("Cidade de Origem:"), 0, 0)
        self.start_city_combo = QComboBox()
        self.start_city_combo.addItems(sorted(CITIES.keys()))
        cities_layout.addWidget(self.start_city_combo, 0, 1)
        
        # Cidade de destino
        cities_layout.addWidget(QLabel("Cidade de Destino:"), 1, 0)
        self.goal_city_combo = QComboBox()
        self.goal_city_combo.addItems(sorted(CITIES.keys()))
        self.goal_city_combo.setCurrentText("Bucharest")  # Padrão
        cities_layout.addWidget(self.goal_city_combo, 1, 1)
        
        control_layout.addWidget(cities_group)
        
        # Grupo de algoritmos
        algorithms_group = QGroupBox("Algoritmos de Busca")
        algorithms_layout = QVBoxLayout()
        algorithms_group.setLayout(algorithms_layout)
        
        # Algoritmos não informados
        uninformed_group = QGroupBox("Não Informados (Cegos)")
        uninformed_layout = QVBoxLayout()
        uninformed_group.setLayout(uninformed_layout)
        
        self.bfs_button = QPushButton("Busca em Largura (BFS)")
        self.bfs_button.clicked.connect(lambda: self.run_algorithm("bfs"))
        uninformed_layout.addWidget(self.bfs_button)
        
        self.ucs_button = QPushButton("Busca de Custo Uniforme (UCS)")
        self.ucs_button.clicked.connect(lambda: self.run_algorithm("ucs"))
        uninformed_layout.addWidget(self.ucs_button)
        
        self.dfs_button = QPushButton("Busca em Profundidade (DFS)")
        self.dfs_button.clicked.connect(lambda: self.run_algorithm("dfs"))
        uninformed_layout.addWidget(self.dfs_button)
        
        self.dls_button = QPushButton("Busca em Profundidade Limitada (DLS)")
        self.dls_button.clicked.connect(lambda: self.run_algorithm("dls"))
        uninformed_layout.addWidget(self.dls_button)
        
        self.ids_button = QPushButton("Busca de Aprofundamento Iterativo (IDS)")
        self.ids_button.clicked.connect(lambda: self.run_algorithm("ids"))
        uninformed_layout.addWidget(self.ids_button)
        
        self.bidirectional_button = QPushButton("Busca Bidirecional")
        self.bidirectional_button.clicked.connect(lambda: self.run_algorithm("bidirectional"))
        uninformed_layout.addWidget(self.bidirectional_button)
        
        algorithms_layout.addWidget(uninformed_group)
        
        # Algoritmos informados
        informed_group = QGroupBox("Informados (Heurísticos)")
        informed_layout = QVBoxLayout()
        informed_group.setLayout(informed_layout)
        
        self.greedy_button = QPushButton("Busca Gulosa")
        self.greedy_button.clicked.connect(lambda: self.run_algorithm("greedy"))
        informed_layout.addWidget(self.greedy_button)
        
        self.astar_button = QPushButton("Algoritmo A*")
        self.astar_button.clicked.connect(lambda: self.run_algorithm("astar"))
        informed_layout.addWidget(self.astar_button)
        
        algorithms_layout.addWidget(informed_group)
        
        # Botão para comparar todos os algoritmos
        self.compare_button = QPushButton("Comparar Todos os Algoritmos")
        self.compare_button.clicked.connect(self.compare_algorithms)
        algorithms_layout.addWidget(self.compare_button)
        
        control_layout.addWidget(algorithms_group)
        
        # Painel de visualização (direita)
        visualization_panel = QWidget()
        visualization_layout = QVBoxLayout(visualization_panel)
        splitter.addWidget(visualization_panel)
        
        # Abas para diferentes visualizações
        self.tabs = QTabWidget()
        visualization_layout.addWidget(self.tabs)
        
        # Aba do mapa
        self.map_tab = QWidget()
        map_layout = QVBoxLayout(self.map_tab)
        
        # Canvas para o mapa
        self.map_canvas = MatplotlibCanvas(self.map_tab, width=8, height=6)
        map_layout.addWidget(self.map_canvas)
        
        # Barra de ferramentas para o mapa
        self.map_toolbar = NavigationToolbar(self.map_canvas, self.map_tab)
        map_layout.addWidget(self.map_toolbar)
        
        self.tabs.addTab(self.map_tab, "Mapa")
        
        # Aba de resultados
        self.results_tab = QWidget()
        results_layout = QVBoxLayout(self.results_tab)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        self.tabs.addTab(self.results_tab, "Resultados")
        
        # Aba de métricas
        self.metrics_tab = QWidget()
        metrics_layout = QVBoxLayout(self.metrics_tab)
        
        self.metrics_canvas = MatplotlibCanvas(self.metrics_tab, width=8, height=6)
        metrics_layout.addWidget(self.metrics_canvas)
        
        self.metrics_toolbar = NavigationToolbar(self.metrics_canvas, self.metrics_tab)
        metrics_layout.addWidget(self.metrics_toolbar)
        
        self.tabs.addTab(self.metrics_tab, "Métricas")
        
        # Aba de animação
        self.animation_tab = QWidget()
        animation_layout = QVBoxLayout(self.animation_tab)
        
        self.animation_canvas = MatplotlibCanvas(self.animation_tab, width=8, height=6)
        animation_layout.addWidget(self.animation_canvas)
        
        self.animation_toolbar = NavigationToolbar(self.animation_canvas, self.animation_tab)
        animation_layout.addWidget(self.animation_toolbar)
        
        self.tabs.addTab(self.animation_tab, "Animação")
        
        # Configura o splitter
        splitter.setSizes([300, 900])
        
        # Plota o mapa inicial
        self.plot_initial_map()
    
    def plot_initial_map(self):
        """Plota o mapa inicial."""
        self.map_canvas.ax.clear()
        plot_map(self.graph, self.map_canvas.ax)
        self.map_canvas.draw()
    
    def run_algorithm(self, algorithm_name):
        """Executa o algoritmo selecionado."""
        start = self.start_city_combo.currentText()
        goal = self.goal_city_combo.currentText()
        
        # Executa o algoritmo apropriado
        if algorithm_name == "bfs":
            result = breadth_first_search(self.adjacency_dict, start, goal)
        elif algorithm_name == "ucs":
            result = uniform_cost_search(self.adjacency_dict, start, goal)
        elif algorithm_name == "dfs":
            result = depth_first_search(self.adjacency_dict, start, goal)
        elif algorithm_name == "dls":
            result = depth_limited_search(self.adjacency_dict, start, goal, 10)
        elif algorithm_name == "ids":
            result = iterative_deepening_search(self.adjacency_dict, start, goal)
        elif algorithm_name == "bidirectional":
            result = bidirectional_search(self.adjacency_dict, start, goal)
        elif algorithm_name == "greedy":
            result = greedy_search(self.adjacency_dict, start, goal, STRAIGHT_LINE_TO_BUCHAREST)
        elif algorithm_name == "astar":
            result = a_star_search(self.adjacency_dict, start, goal, STRAIGHT_LINE_TO_BUCHAREST)
        
        # Armazena o resultado
        self.results[algorithm_name] = result
        
        # Atualiza a visualização
        self.update_visualization(result)
    
    def update_visualization(self, result):
        """Atualiza a visualização com os resultados do algoritmo."""
        # Atualiza o mapa
        self.map_canvas.ax.clear()
        if result["path"]:
            highlight_path(self.graph, result["path"], self.map_canvas.ax, 
                          title=f"Caminho encontrado usando {result['algorithm']}")
        else:
            plot_map(self.graph, self.map_canvas.ax, 
                    title=f"Nenhum caminho encontrado usando {result['algorithm']}")
        self.map_canvas.draw()
        
        # Atualiza o texto de resultados
        self.update_results_text(result)
        
        # Atualiza a animação
        self.update_animation(result)
        
        # Muda para a aba do mapa
        self.tabs.setCurrentWidget(self.map_tab)
    
    def update_results_text(self, result):
        """Atualiza o texto de resultados."""
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
    
    def update_animation(self, result):
        """Atualiza a animação da execução do algoritmo."""
        # Limpa a animação anterior se existir
        if hasattr(self, 'animation') and self.animation is not None:
            self.animation = None
            
        # Verifica se há passos para animar
        if not result.get("steps") or len(result.get("steps", [])) == 0:
            return
            
        # Limpa o canvas de animação
        self.animation_canvas.ax.clear()
        
        # Cria a animação
        ani = create_step_by_step_animation(self.graph, result["steps"], 
                                           result["algorithm"], interval=500)
        
        # Atualiza o canvas
        self.animation_canvas.draw()
        
        # Guarda a referência para evitar que seja coletada pelo garbage collector
        self.animation = ani
        
        # Muda para a aba de animação para mostrar o resultado
        self.tabs.setCurrentWidget(self.animation_tab)
    
    def compare_algorithms(self):
        """Compara todos os algoritmos."""
        start = self.start_city_combo.currentText()
        goal = self.goal_city_combo.currentText()
        
        # Executa todos os algoritmos
        self.results = {
            "bfs": breadth_first_search(self.adjacency_dict, start, goal),
            "ucs": uniform_cost_search(self.adjacency_dict, start, goal),
            "dfs": depth_first_search(self.adjacency_dict, start, goal),
            "dls": depth_limited_search(self.adjacency_dict, start, goal, 10),
            "ids": iterative_deepening_search(self.adjacency_dict, start, goal),
            "bidirectional": bidirectional_search(self.adjacency_dict, start, goal),
            "greedy": greedy_search(self.adjacency_dict, start, goal, STRAIGHT_LINE_TO_BUCHAREST),
            "astar": a_star_search(self.adjacency_dict, start, goal, STRAIGHT_LINE_TO_BUCHAREST)
        }
        
        # Cria o DataFrame com as métricas
        df = create_metrics_dataframe(self.results)
        
        # Atualiza o gráfico de métricas
        self.metrics_canvas.ax.clear()
        plot_metrics_comparison(df, self.metrics_canvas.ax)
        self.metrics_canvas.fig.tight_layout()
        self.metrics_canvas.draw()
        
        # Atualiza o texto de resultados com a tabela comparativa
        text = "Comparação de Algoritmos\n\n"
        text += f"Origem: {start}\n"
        text += f"Destino: {goal}\n\n"
        text += create_metrics_table(df)
        self.results_text.setText(text)
        
        # Muda para a aba de métricas
        self.tabs.setCurrentWidget(self.metrics_tab)

def main():
    """Função principal."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # Note o underscore em exec_() para PyQt5

if __name__ == "__main__":
    main()