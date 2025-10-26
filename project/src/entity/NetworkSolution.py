import pandas as pd
import numpy as np
from src.adjacency_matrix import AdjacencyMatrix 
from typing import Tuple, List
import random 

class NetworkSolution:
    """
    Representa una estructura de solución de red para heurísticas de optimización,
    como 'simulated annealing' o algoritmos basados en umbral.
    """

    def __init__(self,
                 graph: AdjacencyMatrix,
                 generator,
                 load
                 ):
        """
        Inicializa la solución de red.
        """
        print("--- [Solution] Iniciando NetworkSolution __init__ ---")
        self.graph = graph
        self.graph_original = graph 
        self.generator = generator
        self.load = load
        self.size_original = graph.get_n_buses()
        self.size = self.size_original

        # Usamos -1.0 como bandera para indicar que el costo no ha sido calculado
        self.cost = np.float64(-1.0) 
        
        # Esto calculará el costo inicial la primera vez que se llame
        self.get_cost() 
        print(f"... [Solution] Costo inicial calculado: {self.cost}")
        
    def neighbour(self, rng: random.Random, ) -> List:
        """
        Genera una solución vecina (remove_node, new_cost, neighborA_index, neighborB_index, suspect_A_B)
        calculando el costo de forma incremental (O(1)).
        """
        # --- CAMBIO: Usar np.float64 para los valores por defecto ---
        neighbour = [-1, np.float64(-1.0), -1, -1, (np.float64(-1.0), np.float64(-1.0))]
        
        # Nodo a eliminar
        C = self.get_random_node(rng)

        if self.graph.is_decisive_branch(self.generator, self.load, C) or \
           self.graph.get_grade_by_node(C) != 2 or \
           self.is_node_nin_graph(C):
            return neighbour # Retorna un vecino inválido
    
        neighbour_c = self.graph.get_neighbors_by_node(C)
        
        A = neighbour_c[0]
        B = neighbour_c[1]

        # --- Lectura de valores actuales (ya son np.float64 de la matriz) ---
        characterized_A_C = [self.get_b(A,C), self.get_b_prime(A,C)]
        characterized_B_C = [self.get_b(B,C), self.get_b_prime(B,C)]
        characterized_A_B = [self.get_b(A,B), self.get_b_prime(A,B)]

        # --- CAMBIO: Usar np.inf y np.float64 ---
        reactancia_A_C = 1 / characterized_A_C[0] if characterized_A_C[0] != 0 else np.inf
        reactancia_B_C = 1 / characterized_B_C[0] if characterized_B_C[0] != 0 else np.inf
        reactancia_A_B = 1 / characterized_A_B[0] if characterized_A_B[0] != 0 else np.float64(0.0)

        sum_reactancias = reactancia_A_C + reactancia_B_C + reactancia_A_B
        
        # --- CAMBIO: Usar np.isinf para la comprobación ---
        if np.isinf(sum_reactancias):
            new_b_AB = np.float64(0.0) 
        else:
            new_b_AB = 1 / sum_reactancias
        
        # --- CAMBIO: Usar np.float64 ---
        suspect_A_B = [new_b_AB + characterized_A_B[1], np.float64(0.0)]
        suspect_A_B[1] = -suspect_A_B[0]

        # --- CÁLCULO DE COSTO INCREMENTAL (O(1)) ---
        
        # --- CÁLCULO DE COSTO INCREMENTAL (O(1)) ---
        
        b_orig_AC = self.get_b_original(A,C)
        b_orig_BC = self.get_b_original(B,C)
        b_orig_AB = self.get_b_original(A,B)

        cost_before_change = abs(characterized_A_C[0] - b_orig_AC) + \
                             abs(characterized_B_C[0] - b_orig_BC) + \
                             abs(characterized_A_B[0] - b_orig_AB)

        cost_after_change = abs(np.float64(0.0) - b_orig_AC) + \
                            abs(np.float64(0.0) - b_orig_BC) + \
                            abs(suspect_A_B[0] - b_orig_AB)
            
        # --- CÁLCULO ---
        
        delta_cost_difference = (cost_after_change - cost_before_change)
        
        new_difference_cost = self.cost + delta_cost_difference

        new_size = self.size - 1
        new_size_penalty = new_size / self.size_original
        
        new_cost = new_difference_cost + new_size_penalty
        
        neighbour = [C, new_cost, A, B, suspect_A_B]

        return neighbour


    def get_b_prime(self, nodeA: int, nodeB: int) -> np.float64:
        return self.graph.get_branch_prime(nodeA, nodeB)
    
    def get_b(self, nodeA: int, nodeB: int) -> np.float64:
        return self.graph.get_branch(nodeA, nodeB)
    
    def get_b_original(self, nodeA: int, nodeB: int) -> np.float64:
        return self.graph_original.get_branch(nodeA,nodeB)
    
    def get_random_node(self, rng : random.Random) -> int:
        """
        Obtiene un ID de bus aleatorio de la red.
        """
        random_index = rng.randint(0, self.size_original - 1)
        return self.graph.buses[random_index]
    
    def set_branch(self, nodeA :int, nodeB : int, branch: Tuple[float,float]):
        self.graph.set_branch(nodeA,nodeB,branch[0])
        self.graph.set_branch_prime(nodeA,nodeB,branch[1])

    def is_node_nin_graph(self,node : int) -> bool:
        return self.graph.get_grade_by_node(node) == 0

    
    def update(self, neighbour : list):
        """
        Actualiza el estado de la red basado en el vecino aceptado.
        donde neighbour = [C,new_cost,A,B,B_ab]
        """
        
        A = neighbour[2]
        B = neighbour[3]
        C = neighbour[0]
        suspect_A_B = neighbour[4]

        zero_branch = (np.float64(0.0), np.float64(0.0))
        self.set_branch(A,C, zero_branch)
        self.set_branch(B,C, zero_branch)
        
        self.set_branch(A,B,suspect_A_B)
        
        # --- ACTUALIZACIÓN DE ESTADO CORREGIDA ---
        
        # 1. Actualiza el tamaño
        self.size -= 1
        
        # 2. Quita el nodo de la lista de disponibles
        self.available_nodes.remove(C) 

        # 3. "Descontamina" el costo
        new_total_cost = neighbour[1]
        new_size_penalty = self.size / self.size_original
        
        # Almacena SOLO el costo de diferencia
        self.cost = new_total_cost - new_size_penalty


    def get_cost(self) -> np.float64:
        """
        Devuelve el costo actual.
        Calcula el costo desde cero si es la primera vez que se llama.
        """
        # --- ¡¡¡BUG CRÍTICO CORREGIDO!!! ---
        # La lógica estaba invertida. 
        # Debe calcular si el costo es igual a la bandera (-1.0).
        if self.cost == -1.0:
            self.calculate_cost()

        return self.cost + (self.size/self.size_original) 

    def calculate_cost(self) -> np.float64:
        """
        Calcula el costo total desde cero O(m) usando matrices dispersas.
        """
        try:
            matrix_current = self.graph.get_matrix_csr()
            matrix_original = self.graph_original.get_matrix_csr()
        except AttributeError:
            matrix_current = self.graph.matrix.tocsr()
            matrix_original = self.graph_original.matrix.tocsr()

        diff_matrix = matrix_current - matrix_original
        
        # .data ya es un array de numpy, .sum() y np.abs() son eficientes
        difference = np.sum(np.abs(diff_matrix.data))
    
        self.cost = difference
        return self.cost