import pandas as pd
import numpy as np

def collapsing_multiedges(df):
    """
    Sums parallel branches (multi-edges) between the same two buses.
    
    This function modifies the input DataFrame in place to add, then remove, 
    temporary columns, and updates the 'suscept' column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with columns 'from_bus', 'to_bus', 'suscept', etc.

    Returns:
    --------
    pd.DataFrame
        The DataFrame with 'suscept' values aggregated for parallel branches.
    """
    df['bus_min'] = df[['from_bus', 'to_bus']].min(axis=1)
    df['bus_max'] = df[['from_bus', 'to_bus']].max(axis=1)
    
    # Sum parallel branches (transform returns the sum broadcasted to all original rows)
    df['suscept'] = df.groupby(['bus_min', 'bus_max'])['suscept'].transform('sum')
    
    # Remove temporary columns
    df.drop(['bus_min', 'bus_max'], axis=1, inplace=True)
    return df

class Branch:
    """
    Class to manage branches of an electrical network and build
    the bus x bus susceptance matrix using dense NumPy arrays.
    """
    
    def __init__(self, df):
        """
        Initialize the Branch class with a DataFrame.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with network branch information.
        """
        self.df = df.copy()
        # Note: The original collapsing_multiedges modifies self.df.copy() in place 
        # but does not aggregate other columns (like 'monitored', 'available')
        # like the AdjacencyMatrix implementation does.
        self.susceptance_collapsed = collapsing_multiedges(self.df) 
        
        self.buses = self._get_unique_buses()
        self.n_buses = len(self.buses)

        # Create bus-to-index mappings and the empty matrix
        self.bus_to_index = {bus: idx for idx, bus in enumerate(self.buses)}
        self.index_to_bus = {idx: bus for idx, bus in enumerate(self.buses)}
        self.matrix = np.zeros((self.n_buses, self.n_buses))
        
        self.fill_matrix()
        
    # Removed create_empty_matrix as its logic is now in __init__
    
    def fill_matrix(self):
        """
        Populates the dense susceptance matrix using the collapsed branch data.
        The matrix is built symmetrically.
        """
        for _, row in self.susceptance_collapsed.iterrows():
            from_bus = row['from_bus']
            to_bus = row['to_bus']
            suscept = row['suscept']
            
            # Convert bus IDs to indices
            i = self.bus_to_index[from_bus]
            j = self.bus_to_index[to_bus]
            
            # Assign the susceptance value (symmetric matrix)
            self.matrix[i, j] = suscept
            self.matrix[j, i] = suscept

    def _get_unique_buses(self):
        """
        Gets a sorted list of unique bus IDs from the network data.
        
        Returns:
        --------
        list
            Sorted list of unique bus IDs.
        """
        return sorted(pd.concat([self.df['from_bus'], self.df['to_bus']]).unique())
    
    # Removed _create_bus_to_idx as its logic is now in __init__
    
    def get_matrix(self):
        """
        Returns the DataFrame of branches with aggregated susceptance.
        
        Note: The name is misleading as it returns a DataFrame, not the matrix (self.matrix).
        """
        return self.susceptance_collapsed
    
    def get_matrix_dataframe(self):
        """
        Returns the dense susceptance matrix as a DataFrame with bus IDs as index/columns.
        """
        return pd.DataFrame(
            self.matrix,
            index=self.buses,
            columns=self.buses
        )
    
    def get_buses(self):
        """Returns the list of bus IDs."""
        # The previous version had a duplicated function name with the same signature.
        # Keeping this one as it returns the list of IDs.
        return [int(bus) for bus in self.buses]
    
    def get_bus_index(self, bus_id):
        """
        Gets the matrix index for a given bus ID.
        
        Parameters:
        -----------
        bus_id : int
            Bus ID.
            
        Returns:
        --------
        int
            Matrix index for the bus, or None if not found.
        """
        return self.bus_to_index.get(bus_id)
    
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
            DataFrame with branches connecting the specified buses.
        """
        mask = ((self.df['from_bus'] == bus_from) & (self.df['to_bus'] == bus_to)) | \
            ((self.df['from_bus'] == bus_to) & (self.df['to_bus'] == bus_from))
        return self.df[mask]
    
    def summary(self):
        """Print a network summary."""
        print(f"=== Network Summary ===")
        print(f"Total number of branches: {len(self.df)}")
        print(f"Available branches: {self.df['available'].sum()}")
        print(f"Monitored branches: {self.df['monitored'].sum()}")
        print(f"Number of unique buses: {self.n_buses}")
        print(f"Buses: {self.buses[:10]}{'...' if self.n_buses > 10 else ''}")
        print(f"Matrix dimension: {self.matrix.shape}")