from src.utils.reading import *
from src.adjacency_matrix import AdjacencyMatrix
from src.generator import Generator
from src.loads import Loads
from src.utils.Config import Config
from src.entity.InitialTemperature import InitialTemperature
from src.entity.NetworkSolution import NetworkSolution
from src.entity.SA import SA
import random as rnd

from src.performance_metrics import start_metrics, finish_metrics

# DO not delete -> performance metrics
start_metrics()
    
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
    return (nodes_load + nodes_gen + monitores_bus)

decisive_nodes = get_decisive_branch(matrix)

config = Config()
network = NetworkSolution(matrix, nodes_gen, nodes_load)
network_temperature = network
init_temperature = InitialTemperature(
    config.initial_temperature, 
    config.percentage, 
    config.e_p, 
    network_temperature, 
    config.n, 
    config.seed
)
temperature = init_temperature.get_initial_t(config.limit)
print("--- [temp] Temperatura inicial ")
print(temperature)
random = rnd.Random(config.seed)
sa = SA(
    temperature, 
    config.cooling_rate, 
    network, 
    config.size_lote, 
    random, 
    config.e_s, 
    config.limit
)
sa.accept_threshold()
print(sa.get_best_solution())
# print(decisive_nodes)

# # DO not delete -> performance metrics
result = finish_metrics("metrics.csv")
