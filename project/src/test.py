from utils.reading import *
from adjacency_matrix import AdjacencyMatrix
import numpy as np

# basic dayli-data read
df_branch, df_generator, df_load = get_day_20240521()

matrix = AdjacencyMatrix(df_branch)
# AdjacencyMatrix.print_matrix_info(matrix)
# print(AdjacencyMatrix.get_susceptance(matrix,))
branchx = matrix.get_bus_index(7329)
branchy = matrix.get_bus_index(7328)

susceptance = matrix.get_susceptance(branchx, branchy)
print(susceptance)

susceptance = matrix.get_susceptance(branchy, branchx)
print(susceptance)



print("branchx:", branchx)
print("branchy:", branchy)