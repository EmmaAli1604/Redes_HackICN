from utils.reading import *
from adjacency_matrix import AdjacencyMatrix
from generator import Generator
from loads import Loads
import numpy as np

# basic dayli-data read
df_branch, df_generator, df_load = get_day_20240521()

matrix = AdjacencyMatrix(df_branch)
# AdjacencyMatrix.print_matrix_info(matrix)
# print(AdjacencyMatrix.get_susceptance(matrix,))
branchx = matrix.get_bus_index(7329)
branchy = matrix.get_bus_index(7328)

susceptance = matrix.get_susceptance(branchx, branchy)
# print(susceptance)

susceptance = matrix.get_susceptance(branchy, branchx)
# print(susceptance)

generator = Generator(df_generator)
nodes_gen = generator.get_nodes()
# print(nodes_gen)

load = Loads(df_load)
nodes_load = load.get_nodes() 
# print(nodes_load)

# print("branchx:", branchx)
# print("branchy:", branchy)