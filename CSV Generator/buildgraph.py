from geopy.distance import geodesic
# from params import RADIUS
import pandas as pd
from datetime import datetime 

RADIUS = 15

class Node:
    def __init__(self, id):
        self.id = id
        self.is_infected = False
        self.locn_data = []
        self.edge_dict = {}
    def __str__(self):
        return '{}'.format(self.id)

class Graph:
    def __init__(self):
        self.nodes = {}

    def create_edge(self, p1_id, p2_id, time, dist, confidence):
        time = (datetime.fromtimestamp(time[0]/1e3), datetime.fromtimestamp(time[1]/1e3))
        if p2_id in self.nodes[p1_id].edge_dict.keys():
            self.nodes[p1_id].edge_dict[p2_id].append((time, dist, confidence))
        else:
            self.nodes[p1_id].edge_dict[p2_id] = [(time, dist, confidence)]
        
        if p1_id in self.nodes[p2_id].edge_dict.keys():
            self.nodes[p2_id].edge_dict[p1_id].append((time, dist, confidence))
        else:
            self.nodes[p2_id].edge_dict[p1_id] = [(time, dist, confidence)]
            
def create_node(id):
    return Node(id=id)

def average(x1, x2):
    return (x1 + x2)/2

def build_graph(path="results_static_data.csv"):
    graph = Graph()
    df = pd.read_csv(path, header = None, names=['id', 'x', 'y', 't_start', 't_end', 'confi'])
    f = open("results.txt", "w")
    f.write("")
    f.close()
    for _, entry in df.iterrows():
        # print(entry['id'])
        if entry['id'] not in graph.nodes.keys():
            graph.nodes[entry['id']] = create_node(entry['id'])
            print("created node: ", graph.nodes[entry['id']])
            
        graph.nodes[entry['id']].locn_data.append(((entry['t_start'], entry['t_end']), (entry['x'], entry['y'], entry['confi'])))

        for node in graph.nodes.values():
            if entry['id'] != node.id:
                for interval in node.locn_data:
                    if interval[0][0] <= entry['t_start'] and interval[0][1] >= entry['t_end']:
                        dist = geodesic((entry['y'], entry['x']), (interval[1][1], interval[1][0])).meters
                        if dist <= RADIUS:
                            time = (entry['t_start'], entry['t_end'])
                            confidence = entry['confi'] * interval[1][2]
                            graph.create_edge(node.id, entry['id'], time, dist, confidence)
                            x_avg = average(entry['x'], interval[1][0])
                            y_avg = average(entry['y'], interval[1][1])
                            f = open("results.txt", "a")
                            f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(entry['id'], node.id, x_avg, y_avg, datetime.fromtimestamp(time[0]/1e3), datetime.fromtimestamp(time[1]/1e3), confidence, dist))
                            f.close()
                            print("added edge between: ", node.id, entry['id'], " time interval: ", time)

                    elif interval[0][0] >= entry['t_start'] and interval[0][1] <= entry['t_end']:
                        dist = geodesic((entry['y'], entry['x']), (interval[1][1], interval[1][0])).meters 
                        if dist <= RADIUS:
                            time = (interval[0][0], interval[0][1])
                            confidence = entry['confi'] * interval[1][2]
                            graph.create_edge(node.id, entry['id'], time, dist, confidence)
                            x_avg = average(entry['x'], interval[1][0])
                            y_avg = average(entry['y'], interval[1][1])

                            f = open("results.txt", "a")
                            f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(entry['id'], node.id, x_avg, y_avg, datetime.fromtimestamp(time[0]/1e3), datetime.fromtimestamp(time[1]/1e3), confidence, dist))
                            f.close()
                            print("added edge between: ", node.id, entry['id'], " time interval: ", time)

build_graph("results_static_data.csv")
