import numpy as np
import pandas as pd
from scipy import sparse

class AdjacencyMatrix:

    def __init__(self, df):
        self.df = df.copy()
        self.susceptance_collapsed = self._collapsing_multiedges(self.df)
        self.buses = self._get_unique_buses()
        self.n_buses = len(self.buses)
        self.bus_to_index = {bus: idx for idx, bus in enumerate(self.buses)}
        self.matrix = self._build_sparse_matrix()
        self.matrix_b_prime = self._build_matrix_b_prime()

    def _build_matrix_b_prime(self):
        row_sums = self.matrix.sum(axis=1)
        diag_values = np.asarray(row_sums).flatten()
        D = sparse.diags(diag_values, format='csr')
        A = -self.matrix + D

        return A
    
    def _collapsing_multiedges(self, df):
        df_collapsed = df.copy()
        df_collapsed['bus_min'] = df_collapsed[['from_bus', 'to_bus']].min(axis=1)
        df_collapsed['bus_max'] = df_collapsed[['from_bus', 'to_bus']].max(axis=1)
        df_collapsed['suscept'] = df_collapsed.groupby(['bus_min', 'bus_max'])['suscept'].transform('sum')
        df_collapsed.drop(['bus_min', 'bus_max'], axis=1, inplace=True)
        return df_collapsed
    
    def _build_sparse_matrix(self):
        df = self.susceptance_collapsed
        
        # Vectorizar: convertir todos los buses a índices de una vez
        from_indices = df['from_bus'].map(self.bus_to_index).values
        to_indices = df['to_bus'].map(self.bus_to_index).values
        susceptances = df['suscept'].values
        
        # Crear arrays para matriz simétrica
        row_indices = np.concatenate([from_indices, to_indices])
        col_indices = np.concatenate([to_indices, from_indices])
        data = np.concatenate([susceptances, susceptances])
        
        # Crear matriz COO y convertir a CSR (más eficiente para operaciones)
        matrix_coo = sparse.coo_matrix(
            (data, (row_indices, col_indices)),
            shape=(self.n_buses, self.n_buses)
        )
        
        return matrix_coo.tocsr()
    
    def index_to_bus(self, index):
        """Convierte un índice de la matriz a su bus correspondiente."""
        if index < 0 or index >= self.n_buses:
            raise IndexError(f"Índice {index} fuera de rango [0, {self.n_buses-1}]")
        return self.buses[index]
    
    def get_bus_index(self, bus):
        """Convierte un bus a su índice correspondiente en la matriz."""
        if bus not in self.bus_to_index:
            raise KeyError(f"Bus {bus} no encontrado en la red")
        return self.bus_to_index[bus]
    
    def print_matrix_info(self):
        """Imprime información útil sin cargar toda la matriz"""
        print(f"Dimensiones: {self.matrix.shape}")
        print(f"Elementos no-cero: {self.matrix.nnz}")
        print(f"Densidad: {self.matrix.nnz / (self.matrix.shape[0]**2) * 100:.4f}%")
        print(f"Memoria: {self.matrix.data.nbytes / 1024**2:.2f} MB")
        print(f"\nEstadísticas de valores:")
        print(f"  Min: {self.matrix.data.min()}")
        print(f"  Max: {self.matrix.data.max()}")
        print(f"  Media: {self.matrix.data.mean()}")
    
    def print_submatrix(self, bus_list):
        """Imprime submatrix para buses específicos"""
        indices = [self.bus_to_index[bus] for bus in bus_list]
        submatrix = self.matrix[np.ix_(indices, indices)].toarray()
        df = pd.DataFrame(submatrix, 
                        index=bus_list, 
                        columns=bus_list)
        print(df)
    
    def get_susceptance(self, idx1, idx2):
        # Parameters:
        # -----------
        # idx1 : int
        #     Índice del primer bus
        # idx2 : int
        #     Índice del segundo bus
            
        # Returns:
        # --------
        # float
        #     susceptance value.
        if idx1 < 0 or idx1 >= self.n_buses or idx2 < 0 or idx2 >= self.n_buses:
            raise IndexError(f"Índices fuera de rango [0, {self.n_buses-1}]")
        
        return self.matrix[idx1, idx2]

    def get_bus_from_index(self, idx):
        return self.buses[idx]

    def get_n_buses(self):
        return self.n_buses

    def _get_unique_buses(self):
        """
        Get sorted list of unique buses from the network.
        
        Returns:
        --------
        list
            Sorted list of unique bus IDs
        """
        return sorted(pd.concat([self.df['from_bus'], self.df['to_bus']]).unique())
    
    # def _create_bus_to_idx(self):
    #     """
    #     Create a dictionary mapping bus IDs to matrix indices.
        
    #     Returns:
    #     --------
    #     dict
    #         Dictionary {bus_id: matrix_index}
    #     """
    #     # print(idx for idx, bus in enumerate(self.buses))
    #     return {bus: idx for idx, bus in enumerate(self.buses)}
    
    def get_matrix(self):
        """Return the susceptance matrix."""
        return self.susceptance_collapsed
    
    def get_matrix_dataframe(self):
        """
        Return the susceptance matrix as a DataFrame with bus indices.
        """
        return pd.DataFrame(
            self.matrix
            # index=self.buses,
            # columns=self.buses
        )
    
    def getMonitoredBranch(self):
        """
        Returns a list of unique buses from monitored branches.
        
        Returns:
            list: Unique buses (from_bus and to_bus) where monitored is True
        """
        # Filter rows where monitored is True
        monitored = self.df[self.df['monitored'] == True]
        
        # Extract unique values from both from_bus and to_bus columns
        return pd.unique(monitored[['from_bus', 'to_bus']].values.ravel()).tolist()

    def is_decisive_branch(self, gen_node, load_node, from_bus, to_bus):
        """
        Determines if a branch is decisive based on whether the buses are in generation nodes,
        load nodes, or are being monitored.

        Do not use index, it requires buses
        
        Parameters:
        -----------
        gen_node : list of int
            List of generation nodes
        load_node : list of int
            List of load nodes
        from_bus : int
            Origin bus
        to_bus : int
            Destination bus
            
        Returns:
        --------
        bool
            False if NONE of the buses are in the lists NOR monitored, True otherwise
        """
        # Convert lists to sets once for O(1) lookup (do this in __init__ if possible)
        gen_set = set(gen_node)
        load_set = set(load_node)
        
        # Quick check: if any bus is in gen or load nodes, return True immediately
        if from_bus in gen_set or from_bus in load_set or to_bus in gen_set or to_bus in load_set:
            return True
        
        # Check monitored status using vectorized operations
        # Use bitwise OR for better performance
        mask_buses = ((self.df['from_bus'] == from_bus) | (self.df['to_bus'] == from_bus) |
                    (self.df['from_bus'] == to_bus) | (self.df['to_bus'] == to_bus))
        
        # If any matching row has monitored = True, return True
        if mask_buses.any() and self.df.loc[mask_buses, 'monitored'].any():
            return True
        
        # None of the conditions met, return False
        return False


    def get_buses(self):
        """Return the list of buses."""
        return [int(bus) for bus in self.buses]
    
    # def get_bus_index(self, bus_id):
    #     """
    #     Get the matrix index for a given bus ID.
        
    #     Parameters:
    #     -----------
    #     bus_id : int
    #         Bus ID
            
    #     Returns:
    #     --------
    #     int
    #         Matrix index for the bus
    #     """
    #     return self.bus_to_idx.get(bus_id)
    
    def get_branch_info(self, bus_from, bus_to):
        """
        Get information about branch(es) between two buses.
        
        Parameters:
        -----------
        bus_from : int
            Origin bus
        bus_to : int
            Destination bus
            
        Returns:
        --------
        pd.DataFrame
            DataFrame with branches connecting the specified buses
        """
        mask = ((self.df['from_bus'] == bus_from) & (self.df['to_bus'] == bus_to)) | \
            ((self.df['from_bus'] == bus_to) & (self.df['to_bus'] == bus_from))
        return self.df[mask]
    
    def get_branch(self, bus_from, bus_to) -> float:
        return self.matrix[bus_from,bus_to]
    
    def get_branch_prime(self,bus_from,bus_to) -> float:
        return self.matrix_b_prime[bus_from,bus_to]

    
    def set_branch(self, bus_from: int, bus_to: int, status: float):
        """Set the susceptance value between two buses."""
        self.matrix[bus_from, bus_to] = status
        self.matrix[bus_to, bus_from] = status
    
    def set_branch_prime(self, bus_from: int, bus_to: int, status : float):
        self.matrix_b_prime[bus_from,bus_to] = status
        self.matrix_b_prime[bus_from,bus_to] = status 

    def get_neighbors_by_node(self, bus: int):
        """Get neighboring buses for a given bus index."""
        row = self.matrix.getrow(bus)
        neighbors = row.nonzero()[1].tolist()
        return neighbors

    def get_grade_by_node(self, bus: int):
        """Get the degree (number of connections) for a given bus index."""
        return len(self.get_neighbors_by_node(bus))

    def summary(self):
        """Print a network summary."""
        print(f"=== Network Summary ===")
        print(f"Total number of branches: {len(self.df)}")
        print(f"Available branches: {self.df['available'].sum()}")
        print(f"Monitored branches: {self.df['monitored'].sum()}")
        print(f"Number of unique buses: {self.n_buses}")
        print(f"Buses: {self.buses[:10]}{'...' if self.n_buses > 10 else ''}")
        print(f"Matrix dimension: {self.susceptance_matrix.shape}")