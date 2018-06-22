from collections import Counter
import numpy as np
import operator

def read_file():
    lista = []
    for i in open('dados/dados_exemplo1.txt'):
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
    #print('nodes: ', nodes)
    for node in nodes:
       #print('node: ', node)
        d = [node] + [0] * len(nodes)

        for row in data:
            if row[0] == node:
                d[row[1]] = row[2]
        #print('d: ', d)
        node_map.append(d)

    return node_map


def iteraction(cost_map, start_n, end_n):
    while is_path_possible(cost_map, [].copy(), start_node, end_n):
        s_global = []
        i = 0
        connections = []
        visited = []
        while i + 1 != end_n:
            print('\ni: ', i)
            print('visited:', visited)
            s_local = []
            node = cost_map[i][0]
            row = cost_map[i]
            for index, cost in enumerate(row[1:]):
                print('index: ', index,  ' cost: ', cost)
                if cost > 0 and index not in visited:
                    print('added')
                    s_local.append([index+1, cost])
            print('s_local: ', s_local)
            if not s_local:
                return cost_map
            np_array_local = np.array(s_local)
            n, con_val = max(np_array_local, key=operator.itemgetter(1))
            print('nodo: ', n, 'max: ', con_val)
            s_global.append(con_val)
            connections.append([node, n])
            visited.append(i)
            i = n - 1

        print('***min: ', min(s_global))
        print('***connections: ', connections)
        update_connections(cost_map, connections, con_val)
    print(cost_map)


def update_connections(cost_map, connections, value):
    for con in connections:
        print('con: ', con)
        row = cost_map[con[0] - 1][1:]  #nodo
        print('row: ', row)
        row[con[1] - 1] = row[con[1] - 1] - value
        row = cost_map[con[1] - 1][1:]  #nodo
        row[con[0] - 1] = row[con[0] - 1] + value
    print('updated cost_map: ', cost_map, '\n')


"Checks if this is possible or not to get from the first to the last node"
def is_path_possible(cost_map, visited, start_n, end_n):
    for row in cost_map[slice(start_n-1, end_n)]:
        visited.append(row[0])               #Add the node index to visited
        for n, i in enumerate(row[1:]):
            print('\nnode: ', n+1)
            print('cost: ', i)
            print('visited: ', visited)

            if i > 0 and (n+1) not in visited: #Cost is greater than 0 and the node index was not visited
                print('cost accepted: ', i)
                if (n+1) == end_n: #node index is equal to the end node
                    return True
                else:
                    if is_path_possible(cost_map, visited.copy(), start_n + n, end_n): #Checks starting from the node index where a connection was found
                        print('true')
                        return True
    print('false')
    return False


data_list = read_file()
print('Data list: ', data_list)
all_nodes = np.concatenate([data_list[:, 0], data_list[:, 1]])
node_dict = Counter(all_nodes).keys()
node_number = len(node_dict)
print('Nodes: ', node_dict)
data_map = create_dictionary(data_list, list(node_dict))
print('\nData Map: ')
for i in data_map:
    print(i)
data_map = np.array(data_map)
start_node = min(data_map[:, 0])
last_node = max(np.array(data_map)[:, 0])
print('start: ', start_node, ' last: ', last_node)
#print('Is path possible: ', is_path_possible(data_map, [], start_node, last_node))
print(iteraction(data_map, start_node, last_node))
