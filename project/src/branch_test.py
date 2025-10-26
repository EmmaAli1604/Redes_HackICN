from utils.reading import *
from adjacency_matrix import AdjacencyMatrix
import numpy as np


df_branch, generator, load = get_day_20240521()

# print(branch.head())

matrix = AdjacencyMatrix(df_branch)
AdjacencyMatrix.print_matrix_info(matrix)
# matrix = Branch.get_matrix_dataframe(branch_)
# buses = Branch.get_buses(branch_)

# print(matrix)
# Branch.print_matrix_info(branch_)
# sus = Branch.get_value(branch_, 1,2)
# print(sus)

# print(branch_.head())
# Mostrar resumen
# print(Branch.summary(branch_))

# Obtener matriz como DataFrame
# print("\n=== Matriz de Susceptancias ===")
# matrix_df = branch.get_matrix_dataframe()
# print(matrix_df)

# Consultar información de una rama específica
# print("\n=== Información rama entre bus 5775 y 5873 ===")
# print(branch.get_branch_info(5775, 5873))