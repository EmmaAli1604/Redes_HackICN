import pandas as pd
from src.adjacency_matrix import AdjacencyMatrix
from src.utils.reading import get_day_20240521
from src.generator import Generator
from scipy import sparse as sp
from typing import Union, Dict, Any, List

def csv_branch_output(graph: AdjacencyMatrix, output_file: str = 'outputs/branches_reduced_output.csv') -> pd.DataFrame:
    """
    Traverses the sparse adjacency matrix and generates a CSV with branch information 
    (one entry per unique branch/edge).
    
    Parameters:
    -----------
    graph : AdjacencyMatrix
        Object containing the adjacency matrix and access methods.
    output_file : str
        Name of the output CSV file.
        
    Returns:
    --------
    pd.DataFrame
        The generated DataFrame of unique branches.
    """
    matrix = graph.matrix
    
    # Convert to COO format for efficient iteration over non-zero elements
    if not sp.isspmatrix_coo(matrix):
        matrix_coo = matrix.tocoo()
    else:
        matrix_coo = matrix
    
    rows_data: List[Dict[str, Any]] = []
    current_id = 1
    
    # has_unavailable = matrix.has_unavailable()
    # if not has_unavailable:
    #     available : 1
    
    for from_idx, to_idx, susceptance_value in zip(matrix_coo.row, matrix_coo.col, matrix_coo.data):
        from_bus = graph.index_to_bus(from_idx)
        to_bus = graph.index_to_bus(to_idx)
        
        # Only store one direction since the matrix is symmetric (from_bus < to_bus)
        if from_bus < to_bus:
            rows_data.append({
                'id': current_id,
                'from_bus': from_bus,
                'to_bus': to_bus,
                'susceptance': susceptance_value
                # 'available': available
            })
            current_id += 1
    
    df_output = pd.DataFrame(rows_data)
    
    df_output['available'] = 1
        
    df_output.to_csv(output_file, index=False)
    
    print(f"CSV generated: {output_file}")
    print(f"Total branches: {len(df_output)}")
    
    return df_output

def output_results(results):
    """Placeholder function to call csv_branch_output with results."""
    csv_branch_output(results)

# Functional code block preserved
df_branch, df_generator, df_load = get_day_20240521()

matrix = AdjacencyMatrix(df_branch)
generator = Generator(df_generator)

csv_branch_output(matrix, output_file='outputs/branches_output.csv')


