from params import INITIAL_INF_POP, C_SIZE, ISOLATION_PROB_THRESHOLD
from geopy.distance import geodesic
from simulation_model import Node, Graph
from collections import deque
import pandas as pd
import gc
import itertools
import random

"""For the purposes of this simulation, the data is assumed to set with timestamp internval of 5 minutes. So, for 20hrs per day, this gives 240 datasnaps per person, per day."""

def simulate(path, population=17000, days=180, tstamp_per_day=240, algo_mode='level3'):
    """path: path to csv file, population: Population of the city simulation must run onto, days: Number of days which simulation must be run, tstamp_per_day: per day per person number of location entries in the csv file, algo_mode: level0, level1, level3, total_isolation [Depth upto which infected population must be isolated]"""
    # create a graph
    print("Creating city model ...")
    graph = Graph(population)
    print("City model created successfully ...")

    # read file by chunks and store data for a day in a register
    print("Initializing Register ...")
    register = []
    for _ in range(tstamp_per_day):
        register.append([])

    print("Register Initialized")
    print("cleaning output file ...")
    f = open("results.txt", "w")
    f.write("")
    f.close()

    """Format of CSV file is important, it is assumed that CSV file is organized in a way that all the entries per person per day is buckted first, and so on."""
    print("starting to read by chunks, block size =", C_SIZE)
    for chunk in pd.read_csv(path, chunksize = C_SIZE, header=None, names=['x', 'y']):
        for idx, entry in chunk.iterrows():
            # Take the input in the register
            register[idx % tstamp_per_day].append({
                "id": (idx // tstamp_per_day) % population, 
                "time": (idx // (population*tstamp_per_day)*1000) + idx % tstamp_per_day,
                "x": entry["x"],
                "y": entry["y"]
            })

            if idx % (population * tstamp_per_day) == 0 and idx != 0 or idx == (population*tstamp_per_day*days) - 1:
              
                # One day has been processed, update the graph based on this and free the memory
                print("Updating graph for day ",idx // (population * tstamp_per_day) ,"...")
                graph.update_graph(register)
                print("Graph updated")

                # Clean the register, get it ready for the next day
                purge_register(register)
                print("Register purged")

                # Run the infection in the city for this day
                print("Infecting the city for day ",idx // (population * tstamp_per_day), "...")
                infect_city(city=graph, curr_day=idx // (population * tstamp_per_day))
                print("City infected successfully")

                # Purge the city for this day
                print("purging city")
                purge_city(city=graph, curr_day=idx // (population * tstamp_per_day), level=algo_mode)

def purge_register(register):
    """Purges the register, i.e. clears up all the lists and collects the garbage memory"""
    for timestamp in register:
        timestamp.clear()
    gc.collect()

def attach_prob(src, trg):
    """Attaches the probability to the nodes wrt the source they got infected [assumed to be]. For now, analysis done on the basis of number of contacts the source made with the target node. [NOTE]: The target node might infect the source node as well, as well as, there might be more than one source infecting the same target, we add up the probabilities, and finally trim it if it exceeds 1."""
    contact_times = len(trg.edge_dict[src.id])

    if contact_times < 3 and contact_times >= 1:
        trg.inf_prob += src.inf_prob/200

    elif contact_times < 7 and contact_times >=3:
        trg.inf_prob += src.inf_prob/100

    elif contact_times < 10 and contact_times >= 7:
        trg.inf_prob += src.inf_prob/60

    elif contact_times < 14 and contact_times >= 10:
        trg.inf_prob += src.inf_prob/20

    else:
        trg.inf_prob += src.inf_prob/10

    # Trimming the excess probability to restrict it exceeding 1.
    trg.inf_prob = min(1, trg.inf_prob)



def bfs(city, inf_node):
    bfs_queue = deque()
    if not inf_node.visited and inf_node.not_isolated(): bfs_queue.append(inf_node)
    inf_node.visited = True

    # print("Inside the bfs visit function", inf_node)

    while bfs_queue:
        u = bfs_queue.popleft()
        for trg_node_ptr in u.edge_dict.keys():
            trg_node = city.nodes[trg_node_ptr]
            if not trg_node.visited and trg_node.not_isolated() and not trg_node.is_infected():
                attach_prob(u, trg_node)
                if trg_node.inf_prob > ISOLATION_PROB_THRESHOLD:
                    infect_node(city, trg_node)
                    trg_node.day_of_isolation = min(u.day_of_isolation + 5, trg_node.day_of_isolation)
                bfs_queue.append(trg_node)
                trg_node.visited = True
    # print("bfs ended for node", inf_node)


def bfs_infection_run(city, infected_sample=None, node=None):
    if infected_sample:
        for inf_node in infected_sample:
            bfs(city, inf_node)
    else:
        bfs(city, node)

def infect_node(city, node):
    if not node.is_infected():
        node.status = 'infected'
        city.healthy -= 1
        city.infected += 1


def infect_city(city, curr_day):
    if curr_day in [0, 1, 2, 3, 4]:
        existing_nodes = [node for node in city.nodes if node and node.not_isolated()]
        # print(city.nodes)
        # print(existing_nodes)
        infected_sample = random.sample(existing_nodes, k=min(INITIAL_INF_POP, len(existing_nodes)))
        # print(infected_sample)
        for node in infected_sample:
            node.day_of_isolation = curr_day
            node.inf_prob = 1
            infect_node(city, node)

        bfs_infection_run(city=city, infected_sample=infected_sample)
    else:
        for node in city.nodes:
            if node and node.not_isolated():
                bfs_infection_run(city=city, node=node)
    city.reset_visit()

def isolate_node(city, node):
    if node.not_isolated():
        print("Isolating ...", node, " current status: ", node.status)
        city.infected -= 1
        city.isolated += 1
        node.status = 'isolated'

def purge_city(city, curr_day, level):
    """Purges the infected city. If infection is found as well as the individual is not isolated till date."""

    inf_sample = [node for node in city.nodes if node and node.is_infected() and node.not_isolated() and node.day_of_isolation == curr_day]
    print(level, " isolation for: ", inf_sample)
    # Isolate only infected people who show infection on curr_day
    if level == 'level0':
        for node in inf_sample:
            isolate_node(city, node)

    # Isolate the infected people as well as their first level contacts
    elif level == 'level1':
        for node in inf_sample:
            isolate_node(city, node)
            for sub_nodes_ptr in node.edge_dict.keys():
                snode = city.nodes[sub_nodes_ptr]
                if snode and snode.not_isolated() and snode.is_infected():
                    isolate_node(city, snode)

    # Isolate upto 3 levels
    elif level == 'level3':
        # init depth variable and run a simple bfs
        depth = 3
        bfs_queue = deque()
        for node in inf_sample:
            if not node.visited and node.not_isolated(): bfs_queue.append(node)
            node.visited = True
            isolate_node(city, node)
            
            while bfs_queue and depth:
                u = bfs_queue.popleft()
                for trg_node_ptr in u.edge_dict.keys():
                    trg_node = city.nodes[trg_node_ptr]
                    if not trg_node.visited and trg_node.not_isolated() and trg_node.is_infected():
                        bfs_queue.append(trg_node)
                        isolate_node(city, trg_node)
                        trg_node.visited = True

                # after 1 level, decrease depth by one
                depth -= 1
                

    elif level == 'total_isolation':
        # Run bfs and isolate all the nodes that should be isolated
        bfs_queue = deque()
        for node in inf_sample:
            if not node.visited and node.not_isolated(): bfs_queue.append(node)
            node.visited = True
            isolate_node(city, node)

            while bfs_queue:
                u = bfs_queue.popleft()
                for trg_node_ptr in u.edge_dict.keys():
                    trg_node = city.nodes[trg_node_ptr]
                    if not trg_node.visited and trg_node.not_isolated() and trg_node.is_infected():
                        bfs_queue.append(trg_node)
                        isolate_node(city, trg_node)
                        trg_node.visited = True
    f = open("results.txt", "a")
    f.write("{0},{1},{2},{3}\n".format(curr_day, city.healthy, city.infected, city.isolated))
    f.close()
    print("day: ", curr_day, " healthy: ", city.healthy, " infected: ", city.infected, " isolated: ", city.isolated)


            
