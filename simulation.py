from params import INITIAL_INF_POP, C_SIZE
from geopy.distance import geodesic
from simulation_model import Node, Graph
from collections import deque
from prob_attach import attach_prob
from purge import purge_city
from spread_infection import infect_city
# from driver import init_cond
import pandas as pd
import gc
import itertools
import random

"""For the purposes of this simulation, the data is assumed to set with timestamp internval of 5 minutes. So, for 20hrs per day, this gives 240 datasnaps per person, per day."""

def simulate(init_cond, output, path, algo_mode, population=100, days=80, tstamp_per_day=40):
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
    print("cleaning output files ...")

    # if(run==0):
    #     f = open("results_{0}.txt".format(algo_mode), "w")
    #     f.write("")
    #     f.close()
    
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

                # marking the infected nodes before infecting the city
                print("Marking the infected nodes for the day, this won't neccessarily increase the current infection count")
                graph.mark_infected_population(curr_day=idx // (population * tstamp_per_day))

                # Run the infection in the city for this day
                print("Infecting the city for day ",idx // (population * tstamp_per_day), "...")
                infect_city(init_cond, city=graph, curr_day=idx // (population * tstamp_per_day), algo_mode=algo_mode)
                print("City infected successfully")

                # Purge the city for this day
                print("purging city")
                purge_city(output, city=graph, curr_day=idx // (population * tstamp_per_day), level=algo_mode)
                
                curr_day = idx // (population * tstamp_per_day)
                if(curr_day == 7):
                    return 0

def purge_register(register):
    """Purges the register, i.e. clears up all the lists and collects the garbage memory"""
    for timestamp in register:
        timestamp.clear()
    gc.collect()

# def random_sim(init_cond, path, n_times=10, algo_mode='level0'):
#     for i in range(n_times):
#         simulate(init_cond, path=path, run=i, algo_mode=algo_mode, population=100, days=80, tstamp_per_day=40)
#         print("Initial_cond: ")
#         print(init_cond)
