import numpy as np
import pandas as pd
from scipy import sparse
from adjacency_matrix import AdjacencyMatrix
from generator import Generator
from loads import Loads
from typing import Dict, Any, Union

class Network:
    """
    Class to integrate and manage the main components of an electrical network:
    the adjacency matrix, generators, and loads.
    """
    
    def __init__(self, adjacency_matrix: AdjacencyMatrix, generator: Generator, loads: Loads):
        """
        Initializes the electrical network with its core components.
        
        Parameters:
        -----------
        adjacency_matrix : AdjacencyMatrix
            Object containing the network's susceptance/adjacency matrix.
        generator : Generator
            Object containing generator information.
        loads : Loads
            Object containing load information.
        """
        self.adjacency_matrix = adjacency_matrix
        self.generator = generator
        self.loads = loads
        
    def get_adjacency_matrix(self) -> AdjacencyMatrix:
        """Returns the AdjacencyMatrix object."""
        return self.adjacency_matrix
    
    def get_generator(self) -> Generator:
        """Returns the Generator object."""
        return self.generator
    
    def get_loads(self) -> Loads:
        """Returns the Loads object."""
        return self.loads
    
    def get_network_summary(self) -> Dict[str, Union[AdjacencyMatrix, Generator, Loads]]:
        """
        Returns a dictionary containing the network's core objects.
        
        Returns:
        --------
        dict : Dictionary with the main objects of the network.
        """
        summary = {
            'adjacency_matrix': self.adjacency_matrix,
            'generator': self.generator,
            'loads': self.loads
        }
        return summary
    
    def __repr__(self) -> str:
        return (f"Network(adjacency_matrix={self.adjacency_matrix}, "
                f"generator={self.generator}, loads={self.loads})")