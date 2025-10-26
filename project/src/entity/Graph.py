from enums.VertexType import *

import numpy as np
import pandas as pd

class Graph:

    def __init__(self, branches: pd.DataFrame, monitored: pd.DataFrame):
        self.vertices = dict()

        ## matriz de aristas
        self.adyacencias = None # Matriz B 

        self.matrizSubscetancia = None # Matriz B'


    def get_susceptancia (self, i: int ,j : int):
        return self.adyacencias[i][j][0]

    def es_monitoreado(self, i:int, j: int):
        return self.adyacencias[i][j][1]

    def get_cost(self):
        pass

    def get_cost(self):
        pass

    def get_reactancia (self, i: int ,j : int):
        return 1 / self.matrizSubscetancia[i][j]

        

        
            

