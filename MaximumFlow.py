from collections import Counter
import numpy as np


def read_file():
    lista = []
    for i in open('dados/dados_ex.txt'):
        line = i.split(' ')[0:3]
        line[2] = line[2].replace('\n', '')
        lista.append(line)

    return np.array(lista)


'''Creates an array where the index 0 is the node name and the [1:] are the values
of the connections with nodes of index number. Example: [1, 3, 0, 5] means
that the node 1 has cost of 3 to connect to node 1, cost 0 to node 2 and cost 5 to node 3'''
def create_dictionary(raw_data, raw_nodes):
    node_map = []
    data = raw_data.astype(np.int)
    nodes = np.array(raw_nodes).astype(np.int)
    for node in nodes:
        d = [node] + [0] * len(nodes)

        for row in data:
            if row[0] == node:
                d[row[1]] = row[2]

        node_map.append(d)

    return node_map


def iteraction(cost_map, start_n, end_n):
    pass


"Checks if this is possibe or not to get from the first to the last node"
def is_path_possible(cost_map, visited, start_n, end_n):
    visited = []
    for row in cost_map[slice(start_n-1, end_n)]:
        for n, i in enumerate(row[1:]):
            if i > 0:
                visited.append(row[0])


data_list = read_file()
all_nodes = np.concatenate([data_list[:, 0], data_list[:, 1]])
node_dict = Counter(all_nodes).keys()
node_number = len(node_dict)
print('Nodes: ', node_dict)
data_map = create_dictionary(data_list, list(node_dict))
print(data_map)
data_map = np.array(data_map)
start_node = min(data_map[:, 0])
last_node = max(np.array(data_map)[:, 0])
print('start: ', start_node, ' last: ', last_node)
is_path_possible(data_map, [], start_node, last_node)
