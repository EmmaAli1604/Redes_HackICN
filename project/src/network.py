import numpy as np
import pandas as pd
from scipy import sparse
from adjacency_matrix import AdjacencyMatrix
from generator import Generator
from loads import Loads

class Network:
    def __init__(self, adjacency_matrix: AdjacencyMatrix, generator: Generator, loads: Loads):
        """
        Inicializa la red eléctrica con sus componentes principales.
        
        Parameters:
        -----------
        adjacency_matrix : AdjacencyMatrix
            Objeto que contiene la matriz de adyacencia de la red
        generator : Generator
            Objeto que contiene información de los generadores
        loads : Loads
            Objeto que contiene información de las cargas
        """
        self.adjacency_matrix = adjacency_matrix
        self.generator = generator
        self.loads = loads
        
    def get_adjacency_matrix(self):
        """Retorna el objeto AdjacencyMatrix"""
        return self.adjacency_matrix
    
    def get_generator(self):
        """Retorna el objeto Generator"""
        return self.generator
    
    def get_loads(self):
        """Retorna el objeto Loads"""
        return self.loads
    
    def get_network_summary(self):
        """
        Retorna un resumen de la red con información básica.
        
        Returns:
        --------
        dict : Diccionario con información resumida de la red
        """
        summary = {
            'adjacency_matrix': self.adjacency_matrix,
            'generator': self.generator,
            'loads': self.loads
        }
        return summary
    
    def __repr__(self):
        return (f"Network(adjacency_matrix={self.adjacency_matrix}, "
                f"generator={self.generator}, loads={self.loads})")