import pandas as pd

class Node:
    def __init__(self, id):
        self.id = id
        self.status = 'healthy'
        self.day_of_isolation = -1
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
                self.nodes[source] = Node(source) if self.nodes[source] is None else pass
                self.nodes[target] = Node(target) if self.nodes[target] is None else pass

                if target in self.nodes[source].edge_dict.keys():
                    self.nodes[source].edge_dict[target].add((row['t_stamp'], row['dist']))
                else:
                    self.nodes[source].edge_dict[target] = {(row['t_stamp'], row['dist'])}

def post_processing(graph):
    pass

def prob_attach(graph):
    pass

def start_process():
    pass

            

def level_one_isolation(graph):
    today = 0
    for node in graph.nodes:
        if node.status != 'isolated':
            if node.is_infected and node.day_of_isolation == today:

                # update the population variables
                graph.healthy -= len(node.edge_set)
                graph.isolated += len(node.edge_set)

                for edge in node.edge_set:
                    # If memory is the priority
                    node.pop(edge)      

                    # If time is the priority
                    node[edge].status = 'isolated'      

    # increment today by some outer function which is calling level_one_isolation at the end of the day
    # today+=1       




    
