import pandas as pd
import numpy as np

def collapsing_multiedges(df):
    df['bus_min'] = df[['from_bus', 'to_bus']].min(axis=1)
    df['bus_max'] = df[['from_bus', 'to_bus']].max(axis=1)
    df['suscept'] = df.groupby(['bus_min', 'bus_max'])['suscept'].transform('sum')
    df.drop(['bus_min', 'bus_max'], axis=1, inplace=True)
    return df

class Branch:
    """
    Class to manage branches of an electrical network and build
    the bus x bus susceptance matrix.
    """
    
    def __init__(self, df):
        """
        Initialize the Branch class with a DataFrame.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with columns: l, branch_name, from_bus, to_bus, 
            suscept, available, monitored
        """
        self.df = df.copy()
        self.susceptance_collapsed = collapsing_multiedges(df)
        # self.susceptance_collapsed.to_csv('susceptance_collapsed.csv')
        self.buses = self._get_unique_buses()
        self.n_buses = len(self.buses)
        self.bus_to_idx = self._create_bus_to_idx()  # Create mapping

        self.susceptance_matrix = self._build_susceptance_matrix()

    def _build_susceptance_matrix(self):
        # Inicializar matriz de ceros
        n = self.n_buses
        raiz = int(np.sqrt(n))

        # Verificar si es un cuadrado perfecto
        if raiz * raiz == n:
            matrix = np.array(self.buses).reshape(raiz, raiz)
        else:
            # Si no es cuadrado perfecto, ajustar
            print(f"Advertencia: {n} elementos no forman un cuadrado perfecto")
            # Opción: tomar solo los primeros raiz² elementos
            matrix = np.array(self.buses[:raiz*raiz]).reshape(raiz, raiz)

        print(matrix)
        
        # Llenar matriz iterando sobre las ramas colapsadas
        # for _, row in self.susceptance_collapsed.iterrows():
        #     i = row['from_bus']
        #     j = row['to_bus']
        #     suscept = row['suscept']
            
        #     print("i", i)
        #     print("j", j)

        #     print("suscept", suscept, "\n")

        #     # Simetría
        #     matrix[i, j] = suscept
        #     matrix[j, i] = suscept

        # for idx, row in self.susceptance_collapsed.iterrows():
        #     from_bus = int(row['from_bus'])
        #     to_bus = int(row['to_bus'])
        #     suscept = row['suscept']
            
        #     matrix[from_bus, to_bus] = suscept

        return matrix  # ← ¡Faltaba esto!

    def _get_unique_buses(self):
        """
        Get sorted list of unique buses from the network.
        
        Returns:
        --------
        list
            Sorted list of unique bus IDs
        """
        return sorted(pd.concat([self.df['from_bus'], self.df['to_bus']]).unique())
    
    def _create_bus_to_idx(self):
        """
        Create a dictionary mapping bus IDs to matrix indices.
        
        Returns:
        --------
        dict
            Dictionary {bus_id: matrix_index}
        """
        # print(idx for idx, bus in enumerate(self.buses))

        return {bus: idx for idx, bus in enumerate(self.buses)}
    
    def get_matrix(self):
        """Return the susceptance matrix."""
        return self.susceptance_collapsed
    
    def get_matrix_dataframe(self):
        """
        Return the susceptance matrix as a DataFrame with bus indices.
        """
        return pd.DataFrame(
            self.susceptance_matrix,
            # index=self.buses,
            # columns=self.buses
        )
    
    def get_buses(self):
        """Return the list of buses."""
        return [int(bus) for bus in self.buses]
    
    def get_bus_index(self, bus_id):
        """
        Get the matrix index for a given bus ID.
        
        Parameters:
        -----------
        bus_id : int
            Bus ID
            
        Returns:
        --------
        int
            Matrix index for the bus
        """
        return self.bus_to_idx.get(bus_id)
    
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
    
    def summary(self):
        """Print a network summary."""
        print(f"=== Network Summary ===")
        print(f"Total number of branches: {len(self.df)}")
        print(f"Available branches: {self.df['available'].sum()}")
        print(f"Monitored branches: {self.df['monitored'].sum()}")
        print(f"Number of unique buses: {self.n_buses}")
        print(f"Buses: {self.buses[:10]}{'...' if self.n_buses > 10 else ''}")
        print(f"Matrix dimension: {self.susceptance_matrix.shape}")