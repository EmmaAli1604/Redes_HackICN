import numpy as np
import pandas as pd
from scipy import sparse

class Generator:

    def __init__(self, df):
        self.df = df.copy()
        self._validate_data()
        self.nodes = self._create_nodes_dataframe()
        
    def _validate_data(self):
        """Validates that the DataFrame has the required columns"""
        required_cols = ['gen', 'generator_name', 'n', 'cap']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
    def get_nodes(self):
        return self.nodes['node'].to_list()
    
    def _create_nodes_dataframe(self):
        """Creates a DataFrame with all unique nodes and their properties"""
        # Get unique nodes (excluding NaN)
        unique_nodes = self.df['n'].dropna().unique()
        
        # Create nodes dataframe
        nodes_df = pd.DataFrame({
            'node': sorted(unique_nodes)
        })
        
        # Add generator count per node
        gen_count = self.df.groupby('n').size().reset_index(name='n_generators')
        nodes_df = nodes_df.merge(gen_count, left_on='node', right_on='n', how='left')
        nodes_df.drop('n', axis=1, inplace=True)
        nodes_df['n_generators'] = nodes_df['n_generators'].fillna(0).astype(int)
        
        # Add total capacity per node (groupby automatically skips NaN)
        cap_by_node = self.df.groupby('n')['cap'].sum().reset_index(name='total_capacity')
        nodes_df = nodes_df.merge(cap_by_node, left_on='node', right_on='n', how='left')
        nodes_df.drop('n', axis=1, inplace=True)
        nodes_df['total_capacity'] = nodes_df['total_capacity'].fillna(0)
        
        return nodes_df
    
    def update_nodes(self):
        """Updates the nodes dataframe based on current generator data"""
        self.nodes = self._create_nodes_dataframe()
    
    def get_node_info(self, node_id):
        """Gets information for a specific node"""
        result = self.nodes[self.nodes['node'] == node_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_nodes_with_generators(self):
        """Returns nodes that have at least one generator"""
        return self.nodes[self.nodes['n_generators'] > 0].copy()
    
    def get_nodes_without_generators(self):
        """Returns nodes that have no generators"""
        return self.nodes[self.nodes['n_generators'] == 0].copy()
    
    def get_generator(self, gen_id):
        """Gets information for a generator by its ID"""
        result = self.df[self.df['gen'] == gen_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_generators_by_node(self, node_id):
        """Gets all generators connected to a specific node"""
        return self.df[self.df['n'] == node_id].copy()
    
    def set_capacity(self, gen_id, capacity):
        """Sets the capacity of a generator"""
        self.df.loc[self.df['gen'] == gen_id, 'cap'] = capacity
        self.update_nodes()  # Update nodes when capacity changes
        
    def set_capacities(self, capacities_dict):
        """
        Sets multiple capacities
        capacities_dict: dict {gen_id: capacity}
        """
        for gen_id, cap in capacities_dict.items():
            self.df.loc[self.df['gen'] == gen_id, 'cap'] = cap
        self.update_nodes()  # Update nodes after all changes
    
    def get_capacity(self, gen_id):
        """Gets the capacity of a generator"""
        gen = self.get_generator(gen_id)
        return gen['cap'] if gen else None
    
    def get_total_capacity(self):
        """Calculates the total installed capacity (excluding NaN)"""
        return self.df['cap'].sum()
    
    def get_capacity_by_node(self):
        """Returns the total capacity per node"""
        return self.df.groupby('n')['cap'].sum()
    
    def get_generators_without_capacity(self):
        """Returns generators without defined capacity"""
        return self.df[self.df['cap'].isna()].copy()
    
    def create_incidence_matrix(self):
        """
        Creates a generator-node incidence matrix (sparse)
        Returns: sparse matrix where rows=generators, columns=nodes
        """
        gen_ids = self.df['gen'].values
        node_ids = self.df['n'].values
        
        # Create index mappings
        unique_gens = np.unique(gen_ids)
        unique_nodes = np.unique(node_ids[~pd.isna(node_ids)])
        
        gen_to_idx = {g: i for i, g in enumerate(unique_gens)}
        node_to_idx = {n: i for i, n in enumerate(unique_nodes)}
        
        # Prepare data for sparse matrix
        rows = []
        cols = []
        data = []
        
        for _, row in self.df.iterrows():
            if not pd.isna(row['n']):
                rows.append(gen_to_idx[row['gen']])
                cols.append(node_to_idx[row['n']])
                data.append(1)
        
        matrix = sparse.csr_matrix(
            (data, (rows, cols)), 
            shape=(len(unique_gens), len(unique_nodes))
        )
        
        return matrix, unique_gens, unique_nodes
    
    def get_summary(self):
        """Returns a statistical summary of the generators and nodes"""
        summary = {
            'total_generators': len(self.df),
            'total_nodes': len(self.nodes),
            'nodes_with_generators': len(self.get_nodes_with_generators()),
            'generators_with_capacity': self.df['cap'].notna().sum(),
            'total_capacity': self.get_total_capacity(),
            'mean_capacity': self.df['cap'].mean(),
            'max_capacity': self.df['cap'].max(),
            'min_capacity': self.df['cap'].min()
        }
        return summary
    
    def filter_by_capacity_range(self, min_cap=None, max_cap=None):
        """Filters generators by capacity range"""
        filtered = self.df.copy()
        if min_cap is not None:
            filtered = filtered[filtered['cap'] >= min_cap]
        if max_cap is not None:
            filtered = filtered[filtered['cap'] <= max_cap]
        return filtered
    
    def export_to_csv(self, generators_file, nodes_file=None):
        """Exports the data to CSV"""
        self.df.to_csv(generators_file, index=False)
        if nodes_file:
            self.nodes.to_csv(nodes_file, index=False)
    
    def __len__(self):
        """Returns the number of generators"""
        return len(self.df)
    
    def __repr__(self):
        return f"Generator(n_generators={len(self)}, n_nodes={len(self.nodes)})"