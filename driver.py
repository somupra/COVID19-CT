from simulation import simulate, purge_register
from plot import final_plot
from params import INITIAL_INF_POP, C_SIZE
from geopy.distance import geodesic
from simulation_model import Node, Graph
from collections import deque
from purge import purge_city
from multiprocessing import Pool
from plot import final_plot
import pandas as pd
import gc
import itertools
import random
import sys


# simulate(path="../openpflow/test2.csv", population=1000, days=100, tstamp_per_day=80, algo_mode='level0')
# final_plot(path='results_level0.txt', N=200)

# simulate(path="../openpflow/test2.csv", population=1000, days=100, tstamp_per_day=80, algo_mode='level0')
# final_plot(path='results_level0.txt', N=200)

def bfs_for_random_sampling(city, node, contact_set):
    # inf_node = node
    depth = 3
    bfs_queue = deque()
    if not node.visited and node.not_isolated() and node not in contact_set: bfs_queue.append(node)
    node.visited = True
    contact_set.add(node)

    while bfs_queue and depth:
        u = bfs_queue.popleft()
        for trg_node_ptr in u.edge_dict.keys():
            trg_node = city.nodes[trg_node_ptr]
            if not trg_node.visited:
                bfs_queue.append(trg_node)
                contact_set.add(trg_node)
                trg_node.visited = True

        # after 1 level, decrease depth by 1.
        depth -= 1


def get_initial_data(path, INITIAL_INF_POP, days, tstamp_per_day, population):

    # create a graph
    print("Creating city model ...")
    graph = Graph(population)
    print("City model created successfully ...")

    # read file by chunks and store data for a day in a register_init_data
    print("Initializing Register ...")
    register_init_data = []
    for _ in range(tstamp_per_day):
        register_init_data.append([])

    print("Register Initialized")
    initial_data = []
    contact_set = set()

    for chunk in pd.read_csv(path, chunksize = C_SIZE, header=None, names=['x', 'y']):
        for idx, entry in chunk.iterrows():
            # Take the input in the register_init_data
            register_init_data[idx % tstamp_per_day].append({
                "id": (idx // tstamp_per_day) % population, 
                "time": (idx // (population*tstamp_per_day)*1000) + idx % tstamp_per_day,
                "x": entry["x"],
                "y": entry["y"]
            })
            if idx % (population * tstamp_per_day) == 0 and idx != 0 or idx == (population*tstamp_per_day*days) - 1:
              
                # One day has been processed, update the graph based on this and free the memory
                print("Updating graph for day ",idx // (population * tstamp_per_day) ,"...")
                graph.update_graph(register_init_data)
                print("Graph updated")

                # Clean the register_init_data, get it ready for the next day
                purge_register(register_init_data)
                print("Register purged")

                result = []
                print("Updating initial data...")

                for _ in range(INITIAL_INF_POP):
                    choice_array = [node for node in graph.nodes if node and node not in contact_set]
                    init_node = random.choice(choice_array)
                    bfs_for_random_sampling(graph, init_node, contact_set)
                    result.append(init_node.id)

                initial_data.append(result)
                curr_day = idx // (population * tstamp_per_day)
                print("Initial data updated for day :", curr_day, "initial_data is: ", initial_data)
                
                if(curr_day == 5):
                    print("Updated initial data successfully: ", initial_data)
                    return initial_data

def comparison_simulation(_):
    print("Setting Initial Data...")
    init_cond = get_initial_data(path="output1.csv", INITIAL_INF_POP=INITIAL_INF_POP, days=80, tstamp_per_day=40, population=100)
    output = []
    for _ in range(3):
        output.append([])
    
    print("Starting Simulations...")

    simulate(init_cond, output[0], path="output1.csv", algo_mode='level0', population=100, days=80, tstamp_per_day=40)
    print("Final output:", output[0])
    print("Starting Simulations for level 1...") 
    simulate(init_cond, output[1], path="output1.csv", algo_mode='level1', population=100, days=80, tstamp_per_day=40)
    print("Final output:", output[1])
    print("Starting Simulations for level3...") 
    simulate(init_cond, output[2], path="output1.csv", algo_mode='level3', population=100, days=80, tstamp_per_day=40)
    print("Final output:", output[2])
    return output

# sys.stdout = open("test.txt", "w")
# comparison_simulation(1)
# sys.stdout.close()

cores = 4
with Pool(cores) as process:
    final_result = process.map(comparison_simulation,[1]*cores)
    print(final_result)
    algo_modes = ['level0', 'level1', 'level3']
    # clearing output files
    for mode in algo_modes:
        f = open("results_{0}.txt".format(mode), "w")
        f.write("")
        f.close()
    for run in range(cores):
        iterator = 0
        for mode in algo_modes:
            f = open("results_{0}.txt".format(mode), "a")
            curr_res = final_result[run][iterator]
            for i in range(len(curr_res)):
                if(i<(len(curr_res)-1)): 
                    f.write("{0},{1},{2},{3},".format(curr_res[i][0], curr_res[i][1], curr_res[i][2], curr_res[i][3]))
                else:
                    f.write("{0},{1},{2},{3}\n".format(curr_res[i][0], curr_res[i][1], curr_res[i][2], curr_res[i][3]))   
            f.close()
            iterator += 1

    for mode in algo_modes:
        final_plot(path="results_{0}.txt".format(mode), N=100, n_days=7, algo_mode=mode)
    
