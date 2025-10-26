import pandas as pd
import numpy as np
import Graph
from typing import Dict, Tuple

class NetworkSolution:
    """
    Represents a network solution structure for optimization heuristics,
    such as simulated annealing or threshold-based algorithms.
    """

    def __init__(self,
                 vertices: Dict,
                 matrix_b: np.ndarray,
                 matrix_character_b: np.ndarray,
                 graph: Graph,
                 alpha: float):
        """
        Initialize the network solution using a vertex dictionary, numeric and boolean matrices,
        and a normalization coefficient.

        Args:
            vertices (Dict): Dictionary of vertex tuples.
            matrix_b (np.ndarray): NxN float matrix (suspect, modified_suspect, is_graph).
            matrix_character_b (np.ndarray): NxN boolean matrix.
            alpha (float): Normalization factor.
        """
        self.vertices = vertices
        self.graph = graph
        size = len(vertices)

        # Initialize matrix of tuples (float, float, bool)
        self.characterized_matrix = np.empty((size, size, bool), dtype=object)

        # Fill the matrix with (value_b, value_character_b, True)
        for i in range(size):
            for j in range(size):
                self.characterized_matrix[i, j] = (
                    matrix_b[i, j],
                    matrix_character_b[i, j],
                    matrix_b[i,j] != 0
                )

        # Normalization coefficient
        self.normalize = size * size * alpha
        


    def neighbour(self) -> Tuple[str,float]:
        """
        Generate a neighboring solution by applying a small random modification
        to the current network configuration.
        """
        pass

    def update(self, neighbour : Tuple):
        """
        Update the state of a specific vertex or the normalization factor
        depending on the provided parameters.
        """
        
        # Eliminar nodo (neighbour[0] -> nodo:str) de self.vectores

        # Marcar como false a self.characterized_matrix[2] todos las aristas que
        # al vector self.characterized_matrix[vector][i] = self.characterized_matrix[i,vector]
        # = false

        # self.cost = neighour[1]


    def get_cost(self) -> float:
        """
        Compute and return the total cost (e.g., energy, distance, or impedance)
        of the current network configuration.
        """
        
        0.0

