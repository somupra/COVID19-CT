from collections import deque
def isolate_node(city, node, mode='infected'):
    if node.not_isolated():
        print("Isolating ...", node, " current status: ", node.status)
        if mode == 'infected':
            city.infected -= 1
            city.isolated_infected += 1
        else:
            city.healthy -= 1
            city.isolated_healthy += 1
        node.status = 'isolated'

def purge_city(city, curr_day, level):
    """Purges the infected city. If infection is found as well as the individual is not isolated till date."""

    inf_sample = [node for node in city.nodes if node and node.is_infected() and node.not_isolated() and node.day_of_isolation == curr_day]

    print(level, " isolation for: ", inf_sample)
    # Isolate only infected people who show infection on curr_day
    if level == 'level0':
        for node in inf_sample:
            isolate_node(city=city, node=node)
        f = open("results_level0.txt", "a")

    # Isolate the infected people as well as their first level contacts
    elif level == 'level1':
        for node in inf_sample:
            isolate_node(city, node)
            for sub_nodes_ptr in node.edge_dict.keys():
                snode = city.nodes[sub_nodes_ptr]
                if snode and snode.not_isolated():
                    isolate_node(city=city, node=snode, mode=snode.status)
        f = open("results_level1.txt", "a")

    # Isolate upto 3 levels
    elif level == 'level3':
        # init depth variable and run a simple bfs
        depth = 3
        bfs_queue = deque()
        for node in inf_sample:
            if not node.visited and node.not_isolated(): bfs_queue.append(node)
            node.visited = True
            isolate_node(city=city, node=node)
            
            while bfs_queue and depth:
                u = bfs_queue.popleft()
                for trg_node_ptr in u.edge_dict.keys():
                    trg_node = city.nodes[trg_node_ptr]
                    if not trg_node.visited and trg_node.not_isolated():
                        bfs_queue.append(trg_node)
                        isolate_node(city=city, node=trg_node, mode=trg_node.status)
                        trg_node.visited = True

                # after 1 level, decrease depth by one
                depth -= 1
        
        f = open("results_level3.txt", "a")

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
                    if not trg_node.visited and trg_node.not_isolated():
                        bfs_queue.append(trg_node)
                        isolate_node(city=city, node=trg_node, mode=trg_node.status)
                        trg_node.visited = True

        f = open("results_total_isolation.txt", "a")
    if(curr_day < 20):
        f.write("{0},{1},{2},{3},".format(city.healthy, city.infected, city.isolated_healthy, city.isolated_infected))
    elif(curr_day == 20):
        f.write("{0},{1},{2},{3}\n".format(city.healthy, city.infected, city.isolated_healthy, city.isolated_infected))
    f.close()
    
    print("day: ", curr_day, " healthy: ", city.healthy, " infected: ", city.infected, " isolated but healthy: ", city.isolated_healthy, " isolated and infected: ", city.isolated_infected)


            
