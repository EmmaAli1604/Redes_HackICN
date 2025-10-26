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
                 graph: Graph,
                 ):
        """
        Initialize the network solution using a vertex dictionary, numeric and boolean matrices,
        and a normalization coefficient.

        Args:
            vertices (Dict): Dictionary of vertex tuples.
            matrix_b (np.ndarray): NxN float matrix (suspect, modified_suspect, is_graph).
            matrix_character_b (np.ndarray): NxN boolean matrix.
            alpha (float): Normalization factor.
        """
        self.graph = graph
        self.graph.original = graph 
        self.size = graph.getN_buses()

        # Normalization coefficient
        self.normalize = self.size * self.size * 10
        self.cost = -1.0
        
    def neighbour(self, rng: random.Random) -> List[Tuple[int, float, int, int, Tuple[float,float]]]:
        """
        Generate a neighboring solution (remove_node, new_cost, neighborA_index, neighborB_index, suspect_A_B)
        by applying a small random modification to the current network configuration.
        """
        neighbour = [-1, -1.0, -1, -1, -1.0]
        size = self.size
        
        #Nodo a eliminar
        C = self.get_random_node(rng)

        if self.graph.is_important(C) and self.graph.get_grade_by_node(C) != 2 and not(self.is_node_nin_graph(C)):
            return neighbour
    
        neighbour_c = self.graph.get_vecino_by_node(C)
        
        A = neighbour_c[0]
        B = neighbour_c[1]

        #Caracterizacion de los nodos A,B,C y guardarlos
        characterized_A_C = [self.get_b(A,C), self.get_b_prime(A,C)]
        characterized_B_C = [self.get_b(B,C), self.get_b_prime(B,C)]
        characterized_A_B = [self.get_b(A,B), self.get_b_prime(A,B)]

        # Reactancia de A-C y B-C
        reactancia_A_C = 1 / characterized_A_C[0]
        reactancia_B_C = 1 / characterized_B_C[0]
        reactancia_A_B = 1 / characterized_A_B[0]

        # Calculamos el nuevo suspect A y B dado C: B_ab = x_ab+x_ac+x_bc
        suspect_A_B = [1/(reactancia_A_C + reactancia_B_C + reactancia_A_B) + characterized_A_B[1],0]
        # Calculamos el nuevo B' de A y B
        suspect_A_B[1] = -suspect_A_B[0]

        # Actualizamos matrix (simulacion de quitar branch)
        self.set_branch(A,C,[0.0,0.0])
        self.set_branch(B,C,[0.0,0.0])
        self.set_branch(A,B,suspect_A_B)

        diagonal = self.get_b_prime(C,C)
        self.graph.set_branch_prime(C,C,(
            diagonal - (characterized_A_C[1] + characterized_A_B[0] + characterized_B_C[0]) + suspect_A_B[0]
        ))

        old_cost = self.cost
        new_cost = self.get_cost()

        neighbour = [C, new_cost, A,B,suspect_A_B]

        self.cost = old_cost
        self.set_branch(A,C,characterized_A_C)
        self.set_branch(A,B,characterized_A_B)
        self.set_branch(B,C,characterized_B_C)

        return neighbour

    def get_b_prime(self, nodeA: int, nodeB: int) -> float:
        return self.graph.get_branch(nodeA, nodeB)[0]
    
    def get_b(self, nodeA: int, nodeB: int) -> float:
        return self.graph.get_branch(nodeA, nodeB)[0]
    
    def get_b_original(self, nodeA: int, nodeB: int) -> float:
        return self.graph_original.get_branch(nodeA,nodeB)[0]
    
    def get_random_node(self, rng : random.Random) -> int:
        return self.graph.get_node_by_index(rng.randint(0,self.size))
    
    def set_branch(self, nodeA :int, nodeB : int, branch: Tuple[float,float]):
        self.graph.set_branch(nodeA,nodeB,branch[0])
        self.graph.set_branch_prime(nodeA,nodeB,branch[1])

    def is_node_nin_graph(self,node : int) -> bool:
        return self.graph.get_grade_by_node(node) == 0

    
    def update(self, neighbour : list[int,float, int, int,float]):
        """
        Update the state of a specific vertex or the normalization factor
        depending on the provided parameters.

        where neighbour = [C,new_cost,A,B,B_ab]
        """
        
        A = neighbour[2]
        B = neighbour[3]
        C = neighbour[0]
        suspect_A_B = neighbour[4]

        self.set_branch(A,C,[0.0,0.0])
        self.set_branch(B,C,[0.0,0.0])
        self.set_branch(A,B,suspect_A_B)

        self.cost = neighbour[1]

    def get_cost(self) -> float:
        """
        Compute and return the total cost (e.g., energy, distance, or impedance)
        of the current network configuration.
        """

        difference = 0.0
        for i in range(self.size):
            for j in range(self.size):
                if self.get_b(i,j) == 0:
                    continue

                difference += abs(self.get_b(i,j) - self.get_b_original(i,j))
    
        self.cost = difference/self.normalize
        return self.cost


