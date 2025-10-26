from src.utils.reading import *
from src.adjacency_matrix import AdjacencyMatrix
from src.generator import Generator
from src.loads import Loads

# basic dayli-data read
df_branch, df_generator, df_load = get_day_20240521()

matrix = AdjacencyMatrix(df_branch)
generator = Generator(df_generator)
nodes_gen = generator.get_nodes()
# print(nodes_gen)

load = Loads(df_load)
nodes_load = load.get_nodes() 
# print(nodes_load)

def get_decisive_branch(matrix):
    monitores_bus = matrix.getMonitoredBranch()
    return (nodes_load + nodes_gen)

decisive_nodes = get_decisive_branch(matrix)
# print(decisive_nodes)