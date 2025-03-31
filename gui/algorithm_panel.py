"""
Painel de seleção de algoritmos para a interface gráfica.
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QPushButton, 
                            QLabel, QComboBox, QGridLayout, QSpinBox)
from PySide6.QtCore import pyqtSignal

class AlgorithmPanel(QWidget):
    """
    Painel para seleção de algoritmos e parâmetros.
    """
    
    # Sinais
    algorithmSelected = pyqtSignal(str, dict)  # (nome_algoritmo, parâmetros)
    compareRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configurações
        self.algorithm_params = {}
        
        # Configura a interface
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        layout = QVBoxLayout(self)
        
        # Grupo de algoritmos não informados
        uninformed_group = QGroupBox("Algoritmos Não Informados (Cegos)")
        uninformed_layout = QVBoxLayout()
        
        # Botões para algoritmos não informados
        self.bfs_button = QPushButton("Busca em Largura (BFS)")
        self.bfs_button.clicked.connect(lambda: self.select_algorithm("bfs"))
        uninformed_layout.addWidget(self.bfs_button)
        
        self.ucs_button = QPushButton("Busca de Custo Uniforme (UCS)")
        self.ucs_button.clicked.connect(lambda: self.select_algorithm("ucs"))
        uninformed_layout.addWidget(self.ucs_button)
        
        self.dfs_button = QPushButton("Busca em Profundidade (DFS)")
        self.dfs_button.clicked.connect(lambda: self.select_algorithm("dfs"))
        uninformed_layout.addWidget(self.dfs_button)
        
        # DLS com parâmetro de profundidade
        dls_widget = QWidget()
        dls_layout = QGridLayout(dls_widget)
        dls_layout.setContentsMargins(0, 0, 0, 0)
        
        self.dls_button = QPushButton("Busca em Profundidade Limitada (DLS)")
        self.dls_button.clicked.connect(lambda: self.select_algorithm("dls", {"depth_limit": self.dls_depth.value()}))
        dls_layout.addWidget(self.dls_button, 0, 0, 1, 2)
        
        dls_layout.addWidget(QLabel("Limite de Profundidade:"), 1, 0)
        self.dls_depth = QSpinBox()
        self.dls_depth.setRange(1, 100)
        self.dls_depth.setValue(10)
        dls_layout.addWidget(self.dls_depth, 1, 1)
        
        uninformed_layout.addWidget(dls_widget)
        
        # IDS com parâmetro de profundidade máxima
        ids_widget = QWidget()
        ids_layout = QGridLayout(ids_widget)
        ids_layout.setContentsMargins(0, 0, 0, 0)
        
        self.ids_button = QPushButton("Busca de Aprofundamento Iterativo (IDS)")
        self.ids_button.clicked.connect(lambda: self.select_algorithm("ids", {"max_depth": self.ids_max_depth.value()}))
        ids_layout.addWidget(self.ids_button, 0, 0, 1, 2)
        
        ids_layout.addWidget(QLabel("Profundidade Máxima:"), 1, 0)
        self.ids_max_depth = QSpinBox()
        self.ids_max_depth.setRange(1, 100)
        self.ids_max_depth.setValue(20)
        ids_layout.addWidget(self.ids_max_depth, 1, 1)
        
        uninformed_layout.addWidget(ids_widget)
        
        self.bidirectional_button = QPushButton("Busca Bidirecional")
        self.bidirectional_button.clicked.connect(lambda: self.select_algorithm("bidirectional"))
        uninformed_layout.addWidget(self.bidirectional_button)
        
        uninformed_group.setLayout(uninformed_layout)
        layout.addWidget(uninformed_group)
        
        # Grupo de algoritmos informados
        informed_group = QGroupBox("Algoritmos Informados (Heurísticos)")
        informed_layout = QVBoxLayout()
        
        # Seleção de heurística
        heuristic_widget = QWidget()
        heuristic_layout = QGridLayout(heuristic_widget)
        heuristic_layout.setContentsMargins(0, 0, 0, 0)
        
        heuristic_layout.addWidget(QLabel("Heurística:"), 0, 0)
        self.heuristic_combo = QComboBox()
        self.heuristic_combo.addItems(["Distância em Linha Reta", "Personalizada"])
        heuristic_layout.addWidget(self.heuristic_combo, 0, 1)
        
        informed_layout.addWidget(heuristic_widget)
        
        # Botões para algoritmos informados
        self.greedy_button = QPushButton("Busca Gulosa")
        self.greedy_button.clicked.connect(lambda: self.select_algorithm("greedy", {"heuristic": self.heuristic_combo.currentText()}))
        informed_layout.addWidget(self.greedy_button)
        
        self.astar_button = QPushButton("Algoritmo A*")
        self.astar_button.clicked.connect(lambda: self.select_algorithm("astar", {"heuristic": self.heuristic_combo.currentText()}))
        informed_layout.addWidget(self.astar_button)
        
        informed_group.setLayout(informed_layout)
        layout.addWidget(informed_group)
        
        # Botão para comparar todos os algoritmos
        self.compare_button = QPushButton("Comparar Todos os Algoritmos")
        self.compare_button.clicked.connect(self.compareRequested.emit)
        layout.addWidget(self.compare_button)
        
        # Espaço em branco
        layout.addStretch()
    
    def select_algorithm(self, algorithm_name, params=None):
        """
        Emite o sinal de algoritmo selecionado.
        
        Args:
            algorithm_name: Nome do algoritmo.
            params: Dicionário com parâmetros adicionais (opcional).
        """
        if params is None:
            params = {}
        
        self.algorithmSelected.emit(algorithm_name, params)