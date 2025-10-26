import pandas as pd
import numpy as np
import Graph
from typing import Dict, Tuple, List
import random 

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
        self.size = len(vertices)

        # Initialize matrix of tuples (float, float, bool)
        self.characterized_matrix = np.empty((self.size, self.size, bool), dtype=object)

        # Fill the matrix with (value_b, value_character_b, True)
        for i in range(size):
            for j in range(size):
                self.characterized_matrix[i, j] = (
                    matrix_b[i, j],
                    matrix_character_b[i, j],
                    matrix_b[i,j] != 0
                )

        # Normalization coefficient
        self.normalize = self.size * self.size * alpha
        



class NetworkSolution:
    def neighbour(self, rng: random.Random) -> List[Tuple[str, float, int, int, float]]:
        """
        Generate a neighboring solution (remove_node, new_cost, neighborA_index, neighborB_index, suspect_A_B)
        by applying a small random modification to the current network configuration.
        """
        neighbour = ["", -1.0]
        size = self.size

        # Select a random node index to remove
        remove_node_index = rng.randint(0, size - 1)
        remove_node = list(self.vertices.keys())[remove_node_index]

        # Check if node is important or has high degree
        if self.graph.is_important(remove_node) and self.graph.get_grade_by_node(remove_node) != 2:
            return neighbour

        # Find the two connected neighbors
        vecino = [-1, -1]
        for i in range(size):
            if self.characterized_matrix[remove_node_index, i][0] != 0:
                if vecino[0] == -1:
                    vecino[0] = i
                else:
                    vecino[1] = i

        # Retrieve the characterized tuples
        characterized_A_remove_node = self.characterized_matrix[vecino[0], remove_node_index]
        characterized_B_remove_node = self.characterized_matrix[vecino[1], remove_node_index]
        characterized_A_B = self.characterized_matrix[vecino[0], vecino[1]]

        # Compute equivalent reactances
        reactancia_A_remove_node = 1 / characterized_A_remove_node[0]
        reactancia_B_remove_node = 1 / characterized_B_remove_node[0]
        suspect_A_B = reactancia_A_remove_node + reactancia_B_remove_node
        Bp = -1 / suspect_A_B

        # Remove node connections temporarily
        self.characterized_matrix[remove_node_index, vecino[0]] = self.characterized_matrix[vecino[0], remove_node_index] = [0.0, 0.0, False]
        self.characterized_matrix[remove_node_index, vecino[1]] = self.characterized_matrix[vecino[1], remove_node_index] = [0.0, 0.0, False]
        self.characterized_matrix[vecino[0], vecino[1]] = self.characterized_matrix[vecino[1], vecino[0]] = [suspect_A_B, Bp, True]

        # Update diagonal temporarily
        diagonal = self.characterized_matrix[remove_node_index, remove_node_index][1]
        self.characterized_matrix[remove_node_index, remove_node_index][1] = (
            diagonal - (characterized_A_remove_node[1] + characterized_B_remove_node[1] + characterized_A_B[1]) + suspect_A_B
        )

        # Compute cost
        new_cost = self.get_cost()

        # Restore original connections
        self.characterized_matrix[remove_node_index, vecino[0]] = self.characterized_matrix[vecino[0], remove_node_index] = characterized_A_remove_node
        self.characterized_matrix[remove_node_index, vecino[1]] = self.characterized_matrix[vecino[1], remove_node_index] = characterized_B_remove_node
        self.characterized_matrix[vecino[0], vecino[1]] = self.characterized_matrix[vecino[1], vecino[0]] = characterized_A_B
        self.characterized_matrix[remove_node_index, remove_node_index][1] = diagonal

        # Build and return neighbor
        neighbour = [remove_node, new_cost, vecino[0], vecino[1], suspect_A_B]
        return neighbour


    def update(self, neighbour : list[str,float, int, int,float]):
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
        
        difference = 0.0
        for i in range(self.size):
            for j in range(self.size):
                if self.characterized_matrix[i,j][2]:
                    continue

                difference += abs(self.characterized_matrix[i,j][0] - self.graph.get_B(i,j))
    
        return difference/self.normalize


