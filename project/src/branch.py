import pandas as pd
import numpy as np

class Branch:
    """
    Clase para gestionar ramas de una red eléctrica y construir
    la matriz de susceptancias bus x bus.
    """
    
    def __init__(self, df):
        """
        Inicializa la clase Branch con un DataFrame.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame con columnas: l, branch_name, from_bus, to_bus, 
            suscept, available, monitored
        """
        self.df = df.copy()
        self.buses = self._get_unique_buses()
        self.n_buses = len(self.buses)
        self.bus_to_idx = {bus: idx for idx, bus in enumerate(self.buses)}
        self.susceptance_matrix = self._build_susceptance_matrix()
    
    def _get_unique_buses(self):
        """Obtiene la lista ordenada de buses únicos."""
        buses_from = set(self.df['from_bus'].unique())
        buses_to = set(self.df['to_bus'].unique())
        all_buses = sorted(set(buses_from.union(buses_to))) 

        return all_buses
    
    def _build_susceptance_matrix(self):
        """
        Construye la matriz de susceptancias bus x bus.
        
        Returns:
        --------
        np.ndarray
            Matriz de susceptancias de dimensión (n_buses, n_buses)
        """
        # Inicializar matriz con ceros
        matrix = np.zeros((self.n_buses, self.n_buses))
        
        # Iterar sobre cada rama disponible
        for _, row in self.df.iterrows():
            if row['available'] == 1:
                from_idx = self.bus_to_idx[row['from_bus']]
                to_idx = self.bus_to_idx[row['to_bus']]
                suscept = row['suscept']
                
                # Agregar susceptancia a la matriz (simétrica)
                matrix[from_idx, to_idx] += suscept
                matrix[to_idx, from_idx] += suscept
                
                # Diagonal: suma negativa de susceptancias
                matrix[from_idx, from_idx] -= suscept
                matrix[to_idx, to_idx] -= suscept
        return matrix
    
    def get_matrix(self):
        """Retorna la matriz de susceptancias."""
        return self.susceptance_matrix
    
    def get_matrix_dataframe(self):
        """
        Retorna la matriz de susceptancias como DataFrame con índices de buses.
        """
        return pd.DataFrame(
            self.susceptance_matrix,
            index=self.buses,
            columns=self.buses
        )
    
    def get_buses(self):
        """Retorna la lista de buses."""
        return self.buses
    
    def get_branch_info(self, bus_from, bus_to):
        """
        Obtiene información de rama(s) entre dos buses.
        
        Parameters:
        -----------
        bus_from : int
            Bus origen
        bus_to : int
            Bus destino
            
        Returns:
        --------
        pd.DataFrame
            DataFrame con las ramas que conectan los buses especificados
        """
        mask = ((self.df['from_bus'] == bus_from) & (self.df['to_bus'] == bus_to)) | \
               ((self.df['from_bus'] == bus_to) & (self.df['to_bus'] == bus_from))
        return self.df[mask]
    
    def summary(self):
        """Imprime un resumen de la red."""
        print(f"=== Resumen de la Red ===")
        print(f"Número total de ramas: {len(self.df)}")
        print(f"Ramas disponibles: {self.df['available'].sum()}")
        print(f"Ramas monitoreadas: {self.df['monitored'].sum()}")
        print(f"Número de buses únicos: {self.n_buses}")
        print(f"Buses: {self.buses}")
        print(f"Dimensión de matriz: {self.susceptance_matrix.shape}")
