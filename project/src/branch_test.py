from utils.reading import *
from branch import Branch

branch, generator, load = get_day_20240521()

# print(branch.head())

branch_ = Branch(branch)
Branch.summary(branch_)

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