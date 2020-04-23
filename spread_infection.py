from collections import deque
from prob_attach import attach_prob
from params import INITIAL_INF_POP
# from driver import init_cond
import random
from simulation_model import Node

"""Runs BFS on city with surely infected_nodes as root, covers only those nodes which are healthy and not isolated yet"""
def bfs(city, inf_node, curr_day):
    bfs_queue = deque()
    if not inf_node.visited and inf_node.not_isolated(): bfs_queue.append(inf_node)
    inf_node.visited = True

    while bfs_queue:
        u = bfs_queue.popleft()
        for trg_node_ptr in u.edge_dict.keys():
            trg_node = city.nodes[trg_node_ptr]
            if not trg_node.visited and trg_node.not_isolated():
                attach_prob(u, trg_node, curr_day)
                bfs_queue.append(trg_node)
                trg_node.visited = True

"""Places an auxillary call to BFS"""
def bfs_infection_run(city, curr_day, infected_sample=None, node=None):
    if infected_sample:
        for inf_node in infected_sample:
            bfs(city, inf_node, curr_day)
    else:
        bfs(city, node, curr_day)

"""Select nodes which aren't isolated yet and mark them infected for the day -- for 5 days, then afterwards, run a BFS from each node which is not isolated yet."""
def infect_city(init_cond, city, curr_day, algo_mode, run):
    if curr_day in [0, 1, 2, 3, 4]:
        existing_nodes = [node for node in city.nodes if node and node.not_isolated() and not node.is_infected()]
        if(algo_mode == 'level0'):
            infected_sample = random.sample(existing_nodes, k=min(INITIAL_INF_POP, len(existing_nodes)))
            if(curr_day == 1):
                init_cond.update({run: []})
            init_cond[run].append([])
            for init_node in infected_sample:
                init_cond[run][curr_day-1].append(init_node.id)

            # init_cond[run].append(infected_sample)
        else:
            infected_sample = []
            for init_node_id in init_cond[run][curr_day-1]:
                print("Node-id is: ", init_node_id)
                if not city.nodes[init_node_id]:
                    city.nodes[init_node_id] = Node(init_node_id)
                infected_sample.append(city.nodes[init_node_id])
            
            print("Infected sample: ", infected_sample)

        # infected_sample = random.sample(existing_nodes, k=min(INITIAL_INF_POP, len(existing_nodes)))

        for node in infected_sample:
            node.day_of_isolation = curr_day
            node.inf_prob = 1
            node.status = 'infected'
            city.healthy -= 1
            city.infected += 1
        print("Initial_cond: ")
        print(init_cond)
        bfs_infection_run(city=city, infected_sample=infected_sample, curr_day=curr_day)
    else:
        for node in city.nodes:
            if node and node.not_isolated():
                # check if the node is infected and current day is the day of symp. showing for it
                # if node.is_infected() and node.day_of_isolation == curr_day:
                #     city.healthy -= 1
                #     city.infected += 1
                    
                bfs_infection_run(city=city, node=node, curr_day=curr_day)
    
    city.reset_visit()
    return init_cond


