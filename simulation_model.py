from itertools import combinations
from geopy.distance import geodesic
from params import RADIUS
import numpy as np
class Node:
    def __init__(self, id):
        self.id = id
        self.visited = False
        self.status = 'healthy'
        self.day_of_isolation = 1000
        self.inf_prob = 0
        self.edge_dict = {}
    
    def not_isolated(self):
        return self.status != 'isolated'
    
    def mark_infection(self, curr_day):
        """Marks infection for node, given the probability of infection."""
        # check if the node has infection or not
        choices = ["infected", "healthy"]
        status = np.random.choice(choices, 1, p=[self.inf_prob, 1 - self.inf_prob])
        if status == 'infected':
            self.status = 'infected'
            self.inf_prob = 1
            self.day_of_isolation = min(curr_day + 5, self.day_of_isolation)
        print("Marking on day ", curr_day, " : ", self.status)


    def is_infected(self):
        return self.status == "infected"

    def __str__(self):
	    return "NODE: {0}, STAT: {1}".format(self.id, self.status)

class Graph:
    def __init__(self, population):
        self.nodes = [None]*population
        self.healthy = population
        self.infected = 0
        self.isolated_healthy = 0
        self.isolated_infected = 0
    
    def mark_infected_population(self, curr_day):
        to_mark = [node for node in self.nodes if node and not node.is_infected() and node.not_isolated()]
        for node in to_mark:
            node.mark_infection(curr_day)

    def create_edge(self, p1, p2):
        dist = geodesic((p1['y'], p1['x']), (p2['y'], p2['x'])).meters

        if not self.nodes[p1["id"]]:
            # If p1 node has no contacts yet, init it, and add entry of p2 in its edge_dict
            # print(p1, p2)
            self.nodes[p1["id"]] = Node(id=p1["id"])
            self.nodes[p1["id"]].edge_dict[p2["id"]] = [(p2["time"], dist)]
        else:
            # print(p1, p2)
            if p2["id"] in self.nodes[p1["id"]].edge_dict.keys():
                self.nodes[p1["id"]].edge_dict[p2["id"]].append((p2["time"], dist))
            else:
                self.nodes[p1["id"]].edge_dict[p2["id"]] = [(p2["time"], dist)]

        
        if not self.nodes[p2["id"]]:
            # If p2 node has no contacts yet, init it, and add entry of p1 in its edge_dict
            self.nodes[p2["id"]] = Node(id=p2["id"])
            self.nodes[p2["id"]].edge_dict[p1["id"]] = [(p1["time"], dist)]
        else:
            if p1["id"] in self.nodes[p2["id"]].edge_dict.keys():
                self.nodes[p2["id"]].edge_dict[p1["id"]].append((p1["time"], dist))
            else:
                self.nodes[p2["id"]].edge_dict[p1["id"]] = [(p1["time"], dist)]

    def update_graph(self, register):
        i = 1
        for t_stamp in register:
            print("processing timestamp ", i, "...")
            for p1, p2 in combinations(t_stamp, 2):
                if geodesic((p1['y'], p1['x']), (p2['y'], p2['x'])).meters <= RADIUS:
                    self.create_edge(p1, p2)
            i += 1

    def reset_visit(self):
        for node in self.nodes: 
            if node: node.visited = False

