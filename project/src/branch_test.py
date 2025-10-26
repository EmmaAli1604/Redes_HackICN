from utils.reading import *
from adjacency_matrix import AdjacencyMatrix
import numpy as np


df_branch, generator, load = get_day_20240521()

# print(branch.head())

matrix = AdjacencyMatrix(df_branch)
AdjacencyMatrix.print_matrix_info(matrix)
# matrix = Branch.get_matrix_dataframe(branch_)
# buses = Branch.get_buses(branch_)

# # print(matrix)
# # Branch.print_matrix_info(branch_)
# # sus = Branch.get_value(branch_, 1,2)
# # print(sus)

# #print(branch_.head())
# # Mostrar resumen
# print(Branch.summary(branch_))

# # Obtener matriz como DataFrame
# print("\n=== Matriz de Susceptancias ===")
# matrix_df = branch.get_matrix_dataframe()
# print(matrix_df)

# # Consultar información de una rama específica
# print("\n=== Información rama entre bus 5775 y 5873 ===")
# print(branch.get_branch_info(5775, 5873))

# # print("Vecino del nodo 5775:", matrix.get_vecino_by_node(5775))
# # print("Grado del nodo 5775:", matrix.get_grade_by_node(5775))

#Prueba para los metodos de get_grade_by_node y get_vecino_by_node
# df_test = pd.DataFrame({
#     'from_bus': ['A', 'B', 'A'],
#     'to_bus':   ['B', 'C', 'C'],
#     'suscept':  [10, 5, 20]
# })

# network = AdjacencyMatrix(df_test)
# bus_A_idx = network.bus_to_index['A']
# bus_B_idx = network.bus_to_index['B']
# bus_C_idx = network.bus_to_index['C']

# # En este ejemplo: A, B, C. Sus índices serán 0, 1, 2 (o algún orden determinado por _get_unique_buses)

# print(f"A: {bus_A_idx}, B: {bus_B_idx}, C: {bus_C_idx}")

# vecinos_A = network.get_vecino_by_node(bus_A_idx)

# # Los vecinos esperados son los índices de B y C.
# esperado_A = [bus_B_idx, bus_C_idx]

# print("Vecinos de A (índices):", vecinos_A)
# print("Vecinos de A (esperado):", esperado_A)
# print("Num vecinos de A:", network.get_grade_by_node(bus_A_idx))

