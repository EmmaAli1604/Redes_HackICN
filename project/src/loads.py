import numpy as np
import pandas as pd
from scipy import sparse


class Loads:

    def __init__(self, df):
        self.df = df.copy()
        self._validate_data()
        self.nodes = self._create_nodes_dataframe()
        
    def _validate_data(self):
        """Validates that the DataFrame has the required columns"""
        required_cols = ['ld', 'load_name', 'n']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def _create_nodes_dataframe(self):
        """Creates a DataFrame with all unique nodes and their properties"""
        # Get unique nodes (excluding NaN)
        unique_nodes = self.df['n'].dropna().unique()
        
        # Create nodes dataframe
        nodes_df = pd.DataFrame({
            'node': sorted(unique_nodes)
        })
        
        # Add load count per node
        load_count = self.df.groupby('n').size().reset_index(name='n_loads')
        nodes_df = nodes_df.merge(load_count, left_on='node', right_on='n', how='left')
        nodes_df.drop('n', axis=1, inplace=True)
        nodes_df['n_loads'] = nodes_df['n_loads'].fillna(0).astype(int)
        
        return nodes_df
    
    def update_nodes(self):
        """Updates the nodes dataframe based on current load data"""
        self.nodes = self._create_nodes_dataframe()
    
    def get_node_info(self, node_id):
        """Gets information for a specific node"""
        result = self.nodes[self.nodes['node'] == node_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_nodes_with_loads(self):
        """Returns nodes that have at least one load"""
        return self.nodes[self.nodes['n_loads'] > 0].copy()
    
    def get_nodes_without_loads(self):
        """Returns nodes that have no loads"""
        return self.nodes[self.nodes['n_loads'] == 0].copy()
    
    def get_load(self, load_id):
        """Gets information for a load by its ID"""
        result = self.df[self.df['ld'] == load_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_load_by_name(self, load_name):
        """Gets information for a load by its name"""
        result = self.df[self.df['load_name'] == load_name]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_loads_by_node(self, node_id):
        """Gets all loads connected to a specific node"""
        return self.df[self.df['n'] == node_id].copy()
    
    def get_load_count_by_node(self):
        """Returns the load count per node"""
        return self.df.groupby('n').size()
    
    def get_nodes_with_multiple_loads(self, min_loads=2):
        """Returns nodes that have multiple loads (>= min_loads)"""
        load_counts = self.df.groupby('n').size()
        nodes_multiple = load_counts[load_counts >= min_loads].index.tolist()
        return self.nodes[self.nodes['node'].isin(nodes_multiple)].copy()
    
    def get_nodes(self):
        return self.nodes['node'].to_list()
    
    def create_incidence_matrix(self):
        """
        Creates a load-node incidence matrix (sparse)
        Returns: sparse matrix where rows=loads, columns=nodes, and mapping arrays
        """
        load_ids = self.df['ld'].values
        node_ids = self.df['n'].values
        
        # Create index mappings
        unique_loads = np.unique(load_ids)
        unique_nodes = np.unique(node_ids[~pd.isna(node_ids)])
        
        load_to_idx = {ld: i for i, ld in enumerate(unique_loads)}
        node_to_idx = {n: i for i, n in enumerate(unique_nodes)}
        
        # Prepare data for sparse matrix
        rows = []
        cols = []
        data = []
        
        for _, row in self.df.iterrows():
            if not pd.isna(row['n']):
                rows.append(load_to_idx[row['ld']])
                cols.append(node_to_idx[row['n']])
                data.append(1)
        
        matrix = sparse.csr_matrix(
            (data, (rows, cols)), 
            shape=(len(unique_loads), len(unique_nodes))
        )
        
        return matrix, unique_loads, unique_nodes
    
    def get_summary(self):
        """Returns a statistical summary of the loads and nodes"""
        summary = {
            'total_loads': len(self.df),
            'total_nodes': len(self.nodes),
            'nodes_with_loads': len(self.get_nodes_with_loads()),
            'unique_load_names': self.df['load_name'].nunique(),
            'mean_loads_per_node': self.df.groupby('n').size().mean(),
            'max_loads_per_node': self.df.groupby('n').size().max(),
            'min_loads_per_node': self.df.groupby('n').size().min()
        }
        return summary
    
    def filter_loads_by_node_list(self, node_list):
        """Filters loads that are connected to nodes in the provided list"""
        return self.df[self.df['n'].isin(node_list)].copy()
    
    def get_duplicate_nodes(self):
        """Returns nodes that have duplicate loads (same node appearing multiple times)"""
        node_counts = self.df['n'].value_counts()
        duplicate_nodes = node_counts[node_counts > 1].index.tolist()
        return self.df[self.df['n'].isin(duplicate_nodes)].copy()
    
    def export_to_csv(self, loads_file, nodes_file=None):
        """Exports the data to CSV"""
        self.df.to_csv(loads_file, index=False)
        if nodes_file:
            self.nodes.to_csv(nodes_file, index=False)
    
    def __len__(self):
        """Returns the number of loads"""
        return len(self.df)
    
    def __repr__(self):
        return f"Loads(n_loads={len(self)}, n_nodes={len(self.nodes)})"