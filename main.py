import pandas as pd
import random
from collections import deque

class Node:
    def __init__(self, id):
        self.id = id
        self.visited = False
        self.status = 'healthy'
        self.day_of_isolation = 1000
        self.is_infected = False
        self.inf_prob = 0
        self.edge_dict = {}

class Graph:
    def __init__(self, population):
        self.nodes = [None]*population
        self.healthy = population
        self.infected = 0
        self.isolated = 0


    def build(self, path, c_size):
        for chunk in pd.read_csv(path, chunksize = c_size, header=None, names=['s_id', 'd_id', 't_stamp', 'dist']):
            for index, row in chunk.iterrows():
                source, target = row['s_id'], row['d_id']
                self.nodes[source] = Node(source) if self.nodes[source] is None else None 
                self.nodes[target] = Node(target) if self.nodes[target] is None else None

                if target in self.nodes[source].edge_dict.keys():
                    self.nodes[source].edge_dict[target].add((row['t_stamp'], row['dist']))
                    self.nodes[target].edge_dict[source].add((row['t_stamp'], row['dist']))
                else:
                    self.nodes[source].edge_dict[target] = {(row['t_stamp'], row['dist'])}
                    self.nodes[target].edge_dict[source] = {(row['t_stamp'], row['dist'])}

    def reset_visit(self):
        for node in self.nodes: node.visited = False

def attach_prob(trg, src):
    contact_times = len(trg.edge_dict[src.id])

    if contact_times < 3 and contact_times >= 1:
        trg.inf_prob += src.inf_prob/10

    elif contact_times < 7 and contact_times >=3:
        trg.inf_prob += src.inf_prob/8

    elif contact_times < 10 and contact_times >= 7:
        trg.inf_prob += src.inf_prob/5

    elif contact_times < 14 and contact_times >= 10:
        trg.inf_prob += src.inf_prob/3

    else:
        trg.inf_prob += src.inf_prob/1.5

def bfs_non_infected(graph, root=None, sample=None, curr_day=None):
    if sample:
        for inf_node in sample:
            inf_node.status = 'infected'
            inf_node.day_of_isolation = curr_day
            inf_node.is_infected = True
            inf_node.inf_prob = 1
            inf_node.visited = True

            bfs_queue = deque()
            bfs_queue.append(inf_node)
            while bfs_queue:
                u = bfs_queue.popleft()
                for trg_node_ptr in u.edge_dict.keys():
                    trg_node = graph.nodes[trg_node_ptr]
                    if not trg_node.visited and trg_node.status != 'isolated':
                        attach_prob(trg_node, u)
                        if trg_node.inf_prob > 0.6:
                            trg_node.status = 'infected'
                            trg_node.is_infected = True
                            trg_node.day_of_isolation = u.day_of_isolation + 5 if u.day_of_isolation + 5 < trg_node.day_of_isolation else trg_node.day_of_isolation
                        bfs_queue.append(trg_node)
                        trg_node.visited = True

    else:
        inf_node = root
        inf_node.visited = True
        bfs_queue = deque()
        bfs_queue.append(inf_node)
        while bfs_queue:
            u = bfs_queue.popleft()
            for trg_node_ptr in u.edge_dict.keys():
                trg_node = graph.nodes[trg_node_ptr]
                if not trg_node.visited and trg_node.status != 'isolated':
                    attach_prob(trg_node, u)
                    if trg_node.inf_prob > 0.6:
                        trg_node.status = 'infected'
                        trg_node.is_infected = True
                        trg_node.day_of_isolation = u.day_of_isolation + 5 if u.day_of_isolation + 5 < trg_node.day_of_isolation else trg_node.day_of_isolation
                    bfs_queue.append(trg_node)
                    trg_node.visited = True
                    


def prob_attach_preprocess(graph, curr_day):
    if curr_day in [1, 2, 3, 4, 5]:
        infected_sample = random.choices(graph.nodes, k=100)
        bfs_non_infected(graph, infected_sample, curr_day)
        graph.reset_visit()

    else:
        for node in graph.nodes():
            bfs_non_infected(graph, node)
            graph.reset_visit()

                        

        
            
def update_graph(graph, path, c_size):
    for chunk in pd.read_csv(path, chunksize = c_size, header=None, names=['s_id', 'd_id', 't_stamp', 'dist']):
            for index, row in chunk.iterrows():
                source, target = row['s_id'], row['d_id']
                graph.nodes[source] = Node(source) if graph.nodes[source] is None else None
                graph.nodes[target] = Node(target) if graph.nodes[target] is None else None

                if target in graph.nodes[source].edge_dict.keys():
                    graph.nodes[source].edge_dict[target].add((row['t_stamp'], row['dist']))
                    graph.nodes[target].edge_dict[source].add((row['t_stamp'], row['dist']))
                else:
                    graph.nodes[source].edge_dict[target] = {(row['t_stamp'], row['dist'])}
                    graph.nodes[target].edge_dict[source] = {(row['t_stamp'], row['dist'])}


def level_one_isolation(graph, curr_day):
    for node in graph.nodes:
        if node.status != 'isolated':
            if node.is_infected and node.day_of_isolation == curr_day:
                to_isolate = random.choices(node.edge_dict.keys(), k = int(len(node.edge_dict)*0.9)) # Isolate approx 90% of the 1st level nodes
                for ptr in to_isolate:
                    if graph.nodes[ptr].status == 'isolated':
                        continue
                    else:
                        graph.isolated += 1
                        if graph.nodes[ptr].status == 'healthy':
                            graph.healthy -= 1
                        else:
                            graph.infected -= 1
                        graph.nodes[ptr].status = 'isolated'


graph = Graph(20)
graph.build(10000)





    
