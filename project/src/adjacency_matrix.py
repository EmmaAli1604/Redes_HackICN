import numpy as np
import pandas as pd
from scipy import sparse

class AdjacencyMatrix:

    def __init__(self, df):
        print("--- [Matrix] Iniciando AdjacencyMatrix __init__ ---")
        self.df = df.copy()
        # 'susceptance_collapsed' holds the DataFrame after combining parallel branches.
        self.susceptance_collapsed = self._collapsing_multiedges(self.df)
        self.buses = self._get_unique_buses()
        self.n_buses = len(self.buses)
        self.bus_to_index = {bus: idx for idx, bus in enumerate(self.buses)}
        
        # Build sparse matrices (CSR format first for efficient build)
        matrix_csr = self._build_sparse_matrix()
        matrix_b_prime_csr = self._build_matrix_b_prime(matrix_csr)
        
        # Convert to LIL format for efficient element assignment/modification
        self.matrix = matrix_csr.tolil()
        self.matrix_b_prime = matrix_b_prime_csr.tolil()
        
        # self.has_unavailable_branches = self._check_availability() # Cambiamos el nombre del atributo si se quiere.
        self.unavailable_branches_flag = self.has_unavailable() # Usamos un nombre claro
        # print(self.unavailable_branches)
        
    def has_unavailable(self):
        """
        Verifica si hay alguna rama "no disponible" en el sistema.
        
        Una rama se considera 'no disponible' si el valor en la columna "available" 
        es distinto de cero (asumiendo 0 = disponible, distinto de 0 = no disponible).

        Returns:
            bool: True si hay al menos un valor distinto de cero en la columna "available", 
                  False en caso contrario (o si la columna no existe).
        """
        if "available" not in self.df.columns:
            # Si la columna 'available' no existe, asumimos que todas las ramas están disponibles por defecto.
            return False 
        
        # Comprueba si el valor absoluto máximo de la columna 'available' es mayor que un umbral.
        # Si hay CUALQUIER valor distinto de cero, el máximo de los valores absolutos será > 0.
        # Se usa .any() para una verificación booleana directa de si algún elemento es distinto de cero.
        # También se puede usar (self.df["available"] != 0).any()
        return (self.df["available"] != 0).any()
    
    def unavailable_branches(self):
        # ... implementación correcta ...
        return (self.df["available"] != 0).any()
    
    def get_unavailable_branches_flag(self):
        return self.unavailable_branches_flag # Retorna el booleano almacenado

    def _build_matrix_b_prime(self, matrix_csr):
        """
        Builds the B' matrix (Graph Laplacian analog) from the susceptance matrix.
        B' = D - A, where D is the diagonal matrix of row sums (bus degrees/total susceptance)
        and A is the susceptance matrix.
        
        Parameters:
        -----------
        matrix_csr : scipy.sparse.csr_matrix
            The susceptance matrix (A).

        Returns:
        --------
        scipy.sparse.csr_matrix
            The B' matrix.
        """
        # Sum rows to get diagonal elements (total susceptance connected to each bus)
        row_sums = matrix_csr.sum(axis=1)
        diag_values = np.asarray(row_sums).flatten()
        D = sparse.diags(diag_values, format='csr')
        
        # Calculate B' = D - A
        A = -matrix_csr + D

        return A
    
    def _collapsing_multiedges(self, df):
        """
        Sums parallel branches (multi-edges) between the same two buses using groupby().agg().
        This is much faster than transform() and creates a smaller DataFrame.
        The resulting DataFrame is symmetric, with 'from_bus' < 'to_bus'.

        Parameters:
        -----------
        df : pd.DataFrame
            Original DataFrame of branches.

        Returns:
        --------
        pd.DataFrame
            DataFrame with collapsed parallel branches.
        """
        df_copy = df.copy()
        
        # 1. Normalize bus directions for grouping (e.g., 101->102 and 102->101)
        #    Use np.min/max on values for speed
        buses_df = df_copy[['from_bus', 'to_bus']]
        df_copy['bus_1'] = np.min(buses_df.values, axis=1)
        df_copy['bus_2'] = np.max(buses_df.values, axis=1)
        
        # 2. Define aggregation rules.
        aggregations = {
            'suscept': 'sum',
            # 'any' is True if at least one parallel branch is True
            'monitored': 'any',
            'available': 'any'
        }

        # 3. Key operation: use agg()
        df_collapsed = df_copy.groupby(['bus_1', 'bus_2']).agg(aggregations).reset_index()
        
        # 4. Rename columns for _build_sparse_matrix to use
        df_collapsed.rename(columns={'bus_1': 'from_bus', 'bus_2': 'to_bus'}, inplace=True)
        
        return df_collapsed
    
    def _build_sparse_matrix(self):
        """
        Builds the sparse susceptance matrix (A) in COO/CSR format. 
        The matrix is symmetric.
        
        Returns:
        --------
        scipy.sparse.csr_matrix
            The symmetric susceptance matrix.
        """
        df = self.susceptance_collapsed
        
        # Vectorize: convert all bus IDs to indices at once
        from_indices = df['from_bus'].map(self.bus_to_index).values
        to_indices = df['to_bus'].map(self.bus_to_index).values
        susceptances = df['suscept'].values
        
        # Create arrays for the symmetric matrix
        row_indices = np.concatenate([from_indices, to_indices])
        col_indices = np.concatenate([to_indices, from_indices])
        data = np.concatenate([susceptances, susceptances])
        
        # Create COO matrix and convert to CSR (efficient for operations)
        matrix_coo = sparse.coo_matrix(
            (data, (row_indices, col_indices)),
            shape=(self.n_buses, self.n_buses)
        )
        
        return matrix_coo.tocsr()
    
    def index_to_bus(self, index):
        """Converts a matrix index to its corresponding bus ID."""
        if index < 0 or index >= self.n_buses:
            raise IndexError(f"Índice {index} fuera de rango [0, {self.n_buses-1}]")
        return self.buses[index]
    
    def get_bus_index(self, bus):
        """Converts a bus ID to its corresponding matrix index."""
        if bus not in self.bus_to_index:
            raise KeyError(f"Bus {bus} no encontrado en la red")
        return self.bus_to_index[bus]
    
    def print_matrix_info(self):
        """Prints useful information about the sparse matrix."""
        # Note: self.matrix is LIL, but its size/data comes from the underlying CSR build
        print(f"Dimensiones: {self.matrix.shape}")
        print(f"Elementos no-cero: {self.matrix.nnz}")
        print(f"Densidad: {self.matrix.nnz / (self.matrix.shape[0]**2) * 100:.4f}%")
        # Memory usage of the data array in MB
        print(f"Memoria: {self.matrix.data.nbytes / 1024**2:.2f} MB") 
        print(f"\nEstadísticas de valores:")
        # Convert LIL data to numpy array for min/max/mean
        data_values = np.concatenate(self.matrix.data)
        print(f"  Min: {data_values.min()}")
        print(f"  Max: {data_values.max()}")
        print(f"  Media: {data_values.mean()}")
    
    def print_submatrix(self, bus_list):
        """Prints submatrix for specific buses."""
        indices = [self.bus_to_index[bus] for bus in bus_list]
        submatrix = self.matrix[np.ix_(indices, indices)].toarray()
        df = pd.DataFrame(submatrix, 
                        index=bus_list, 
                        columns=bus_list)
        print(df)
    
    def get_susceptance(self, idx1, idx2):
        """
        Gets the susceptance value using matrix indices.
        
        Parameters:
        -----------
        idx1 : int
            Index of the first bus.
        idx2 : int
            Index of the second bus.
            
        Returns:
        --------
        float
            Susceptance value.
        """
        if idx1 < 0 or idx1 >= self.n_buses or idx2 < 0 or idx2 >= self.n_buses:
            raise IndexError(f"Índices fuera de rango [0, {self.n_buses-1}]")
        
        return self.matrix[idx1, idx2]

    def get_bus_from_index(self, idx):
        """Returns the bus ID for a given matrix index."""
        return self.buses[idx]

    def get_n_buses(self):
        """Returns the number of buses."""
        return self.n_buses

    def _get_unique_buses(self):
        """
        Gets a sorted list of unique bus IDs from the network data.
        
        Returns:
        --------
        list
            Sorted list of unique bus IDs.
        """
        return sorted(pd.concat([self.df['from_bus'], self.df['to_bus']]).unique())
    
    def get_matrix(self):
        """
        Returns the DataFrame of branches with collapsed multiedges.
        
        Note: The original function name 'get_matrix' is misleading as it returns a DataFrame, 
        not the sparse matrix (which is self.matrix). Keeping the name to preserve original 
        API behavior.
        """
        return self.susceptance_collapsed
    
    def get_matrix_dataframe(self):
        """
        Returns the susceptance matrix (self.matrix) as a dense pandas DataFrame.
        """
        # Note: sparse LIL matrix doesn't directly convert to DataFrame nicely, 
        # but toarray() works and creates the dense matrix.
        return pd.DataFrame(
            self.matrix.toarray(),
            index=self.buses,
            columns=self.buses
        )
    
    def getMonitoredBranch(self):
        """
        Returns a list of unique bus IDs connected to monitored branches.
        
        Returns:
            list: Unique bus IDs where monitored is True for any connected branch.
        """
        # Filter rows where monitored is True
        monitored = self.df[self.df['monitored'] == True]
        
        # Extract unique values from both from_bus and to_bus columns
        return pd.unique(monitored[['from_bus', 'to_bus']].values.ravel()).tolist()

    def is_decisive_branch(self, gen_node, load_node, bus):
        """
        Determines if a branch connected to 'bus' is 'decisive'.
        A branch is decisive if the 'bus' is a generator or load node, 
        or if any branch connected to 'bus' is monitored.
        
        This method uses bus IDs, not indices.
        
        Parameters:
        -----------
        gen_node : list of int
            List of generation bus IDs.
        load_node : list of int
            List of load bus IDs.
        bus : int
            Bus ID to check.
            
        Returns:
        --------
        bool
            True if any condition is met, False otherwise.
        """
        gen_set = set(gen_node)
        load_set = set(load_node)
        
        # 1. Check if the bus itself is a gen or load node
        if bus in gen_set or bus in load_set:
            return True
        
        # 2. Check monitored status for any branch connected to the bus
        mask_buses = (self.df['from_bus'] == bus) | (self.df['to_bus'] == bus)
        
        # If any matching row has monitored = True, return True
        if mask_buses.any() and self.df.loc[mask_buses, 'monitored'].any():
            return True
        
        # None of the conditions met
        return False

    def get_buses(self):
        """Returns the list of bus IDs."""
        return [int(bus) for bus in self.buses]
    
    def get_branch_info(self, bus_from: int, bus_to: int):
        """
        Gets information about all original branch(es) between two bus IDs.
        
        Parameters:
        -----------
        bus_from : int
            Origin bus ID.
        bus_to : int
            Destination bus ID.
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with all branches connecting the specified buses.
        """
        # Mask for branches in either direction
        mask = ((self.df['from_bus'] == bus_from) & (self.df['to_bus'] == bus_to)) | \
            ((self.df['from_bus'] == bus_to) & (self.df['to_bus'] == bus_from))
        return self.df[mask]
    
    def get_branch(self, bus_from: int, bus_to: int) -> float:
        """Obtains the susceptance value (A matrix entry) using bus IDs."""
        try:
            idx_from = self.bus_to_index[bus_from]
            idx_to = self.bus_to_index[bus_to]
        except KeyError as e:
            raise KeyError(f"Bus ID {e} no encontrado en bus_to_index")
        return self.matrix[idx_from, idx_to]

    def get_branch_prime(self, bus_from: int, bus_to: int) -> float:
        """Obtains the B' matrix value using bus IDs."""
        try:
            idx_from = self.bus_to_index[bus_from]
            idx_to = self.bus_to_index[bus_to]
        except KeyError as e:
            raise KeyError(f"Bus ID {e} no encontrado en bus_to_index")
        return self.matrix_b_prime[idx_from, idx_to]

    def set_branch(self, bus_from: int, bus_to: int, status: float):
        """Sets the susceptance value (A matrix entry) using bus IDs (symmetric)."""
        try:
            idx_from = self.bus_to_index[bus_from]
            idx_to = self.bus_to_index[bus_to]
        except KeyError as e:
            raise KeyError(f"Bus ID {e} no encontrado en bus_to_index")
    
        self.matrix[idx_from, idx_to] = status
        self.matrix[idx_to, idx_from] = status

    def set_branch_prime(self, bus_from: int, bus_to: int, status : float):
        """Sets the B' matrix value using bus IDs (symmetric)."""
        try:
            idx_from = self.bus_to_index[bus_from]
            idx_to = self.bus_to_index[bus_to]
        except KeyError as e:
            raise KeyError(f"Bus ID {e} no encontrado en bus_to_index")

        self.matrix_b_prime[idx_from, idx_to] = status
        self.matrix_b_prime[idx_to, idx_from] = status 

    def get_neighbors_by_node(self, bus: int):
        """Obtains the bus IDs of neighbors for a given bus ID."""
        try:
            # 1. Convert bus ID to matrix index
            idx = self.bus_to_index[bus]
        except KeyError:
            return [] # Bus does not exist, no neighbors
    
        # 2. Get the row using the INDEX
        row = self.matrix.getrow(idx)
    
        # 3. Get the INDICES of the neighbors (column indices of non-zero elements)
        neighbor_indices = row.nonzero()[1].tolist()
    
        # 4. Convert neighbor INDICES back to BUS IDs
        return [self.buses[i] for i in neighbor_indices]

    def get_grade_by_node(self, bus: int):
        """Obtains the degree (number of connections) for a given bus ID."""
        try:
            # 1. Convert bus ID to matrix index
            idx = self.bus_to_index[bus]
        except KeyError:
            return 0 # Bus does not exist, degree 0
    
        # 2. .nnz (Number of Non-Zero) is the fastest way to get the degree from a sparse row
        return self.matrix.getrow(idx).nnz

    def summary(self):
        """Prints a network summary."""
        print(f"=== Network Summary ===")
        print(f"Total number of branches (original): {len(self.df)}")
        print(f"Total number of collapsed branches (edges): {len(self.susceptance_collapsed)}")
        print(f"Available branches: {self.df['available'].sum()}")
        print(f"Monitored branches: {self.df['monitored'].sum()}")
        print(f"Number of unique buses: {self.n_buses}")
        print(f"Buses: {self.buses[:10]}{'...' if self.n_buses > 10 else ''}")
        print(f"Matrix dimension: {self.matrix.shape}")