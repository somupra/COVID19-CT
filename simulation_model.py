from itertools import combinations
from geopy.distance import geodesic
from params import RADIUS
class Node:
    def __init__(self, id):
        self.id = id
        self.visited = False
        self.status = 'healthy'
        self.day_of_isolation = 1000
        self.inf_prob = 0
        self.edge_dict = {}
    def not_isolated(self):
        return self.status == 'isolated'
    def is_infected(self):
        return self.status == 'infected'
    def __str__(self):
	    return "NODE: {0}".format(self.id)

class Graph:
    def __init__(self, population):
        self.nodes = [None]*population
        self.healthy = population
        self.infected = 0
        self.isolated = 0
    
    def create_edge(self, p1, p2):
        dist = geodesic((p1['y'], p1['x']), (p2['y'], p2['x'])).meters

        if not self.nodes[p1["id"]]:
            # If p1 node has no contacts yet, init it, and add entry of p2 in its edge_dict
	        print(p1, p2)
            self.nodes[p1["id"]] = Node(id=p1["id"])
            self.nodes[p1["id"]].edge_dict[p2["id"]] = [(p2["time"], dist)]
        else:
	        print("adding something")
            print(self.nodes[p1["id"]].edge_dict)
            self.nodes[p1["id"]].edge_dict[p2["id"]].append((p2["time"], dist))

        
        if not self.nodes[p2["id"]]:
            # If p2 node has no contacts yet, init it, and add entry of p1 in its edge_dict
            self.nodes[p2["id"]] = Node(id=p2["id"])
            self.nodes[p2["id"]].edge_dict[p1["id"]] = [(p1["time"], dist)]
        else:
            self.nodes[p2["id"]].edge_dict[p1["id"]].append((p1["time"], dist))


    def update_graph(self, register):
        for t_stamp in register:
            for p1, p2 in combinations(t_stamp, 2):
                if geodesic((p1['y'], p1['x']), (p2['y'], p2['x'])).meters <= RADIUS:
                    self.create_edge(p1, p2)

    def reset_visit(self):
        for node in self.nodes: node.visited = False

