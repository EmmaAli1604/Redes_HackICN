import pandas as pd
from adjacency_matrix import AdjacencyMatrix
from utils.reading import get_day_20240521
from generator import Generator
from scipy import sparse as sp

def csv_branch_output(graph, output_file='outputs/branches_reduced_output.csv'):
    """
    Recorre la matriz de adyacencia sparse y genera un CSV con información de ramas.
    
    Parameters:
    -----------
    graph : AdjacencyMatrix
        Objeto con la matriz de adyacencia y métodos de acceso
    output_file : str
        Nombre del archivo CSV de salida
    """
    matrix = graph.matrix
    
    # Convertir a formato COO (Coordinate) para iteración eficiente
    if not sp.isspmatrix_coo(matrix):
        matrix_coo = matrix.tocoo()
    else:
        matrix_coo = matrix
    
    # Listas para almacenar los datos
    rows_data = []
    id = 1
    # Iterar sobre elementos no-cero de la matriz
    for from_idx, to_idx, susceptance_value in zip(matrix_coo.row, matrix_coo.col, matrix_coo.data):
        # Convertir índices a nombres de buses usando el método que ya existe
        from_bus = graph.index_to_bus(from_idx)
        to_bus = graph.index_to_bus(to_idx)
        
        # Como la matriz es simétrica, solo guardamos una dirección (evitar duplicados)
        # Solo guardamos cuando from_bus < to_bus
        if from_bus < to_bus:
            rows_data.append({
                'id': id,
                'from_bus': from_bus,
                'to_bus': to_bus,
                'susceptance': susceptance_value
            })
            id += 1
    
    # Crear DataFrame y guardar a CSV
    df_output = pd.DataFrame(rows_data)
    df_output.to_csv(output_file, index=False)
    
    print(f"CSV generado: {output_file}")
    print(f"Total de ramas: {len(df_output)}")
    
    return df_output

def output_results(results):
    csv_branch_output(results)

df_branch, df_generator, df_load = get_day_20240521()

matrix = AdjacencyMatrix(df_branch)
generator = Generator(df_generator)

csv_branch_output(matrix, output_file='outputs/branches_output.csv')