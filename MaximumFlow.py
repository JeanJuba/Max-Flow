from collections import Counter
import numpy as np
import operator


def read_file():
    lista = []
    for i in open('dados/dados_exemplo2.txt'):
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
    while is_path_possible(cost_map, [].copy(), start_n, end_n):
        print('entrou')
        s_global = []
        i = 0
        connections = []
        visited = []

        while i + 1 != end_n:
            #print('\ni: ', i)
            #print('visited:', visited)
            node = cost_map[i][0]
            row = cost_map[i][1:]
            #print('row list: ', row)
            row_max = get_row_max(cost_map, i, visited.copy(), end_n-1)
            #print('****row: ', i, ' row_max_index: ', row_max, ' row_max_val: ', row[row_max])
            s_global.append(row[row_max])
            connections.append([node, row_max + 1])
            visited.append(i)
            i = row_max

        min_cost = min(s_global)
        #print('s_global: ', s_global)
        #print('***min: ', min_cost)
        #print('***connections: ', connections)
        update_connections(cost_map, connections, min_cost)
        #exit()
    #print(cost_map)
    return cost_map


def update_connections(cost_map, connections, value):
    old_cost = cost_map.copy()
    print('\nvalue: ', value)
    for con in connections:
        print('con: ', con)
        row = cost_map[con[0] - 1][1:]  #nodo
        #print('1 - row before: ', row)
        row[con[1] - 1] = row[con[1] - 1] - value
        #print('1 - row after:  ', row)
        row = cost_map[con[1] - 1][1:]  #nodo
        #print('2 - row before: ', row)
        row[con[0] - 1] = row[con[0] - 1] + value
        #print('2 - row after:  ', row)
    #print('old cost map: \n', old_cost, '\n')
    print('updated cost_map:\n ', cost_map, '\n')


"Checks if this is possible or not to get from the first to the last node"
def is_path_possible(cost_map, visited, start_n, end_n):

    for row in cost_map[slice(start_n-1, end_n)]:
        #print('row: ', row)
        visited.append(row[0])               #Add the node index to visited
        for n, i in enumerate(row[1:]):
            found_any = False
           #print('\nnode: ', n+1)
           #print('cost: ', i)
           #print('visited: ', visited)
            #print('i: ', i, ' visited: ', visited)
            if i > 0 and (n+1) not in visited: #Cost is greater than 0 and the node index was not visited
                found_any = True
                print('n: ',n ,' cost accepted: ', i)
                if (n+1) == end_n: #node index is equal to the end node
                    print('****Path possible: true')
                    return True
                else:
                    if is_path_possible(cost_map, visited.copy(), start_n + n, end_n): #Checks starting from the node index where a connection was found
                        print('****Path possible: true')
                        return True
        if not found_any:
            print('****Path possible: false, found none')
            return False
    print('****Path possible: false')
    return False


def get_row_max(costs, node, visited, end_node ):
    #print('\nNode: ', node)
    visited.append(node)
    #print('Visited: ', visited)
    local_connections = []
    #dead_end = True
    list = np.array(costs[node][1:].copy())
    #print('list: ', list)
    while np.any(list):
        local_connections = []
        for index, cost in enumerate(list):
            if cost > 0 and index not in visited:
                local_connections.append([index, cost])

        #print('Local connections: ', local_connections)
        if len(local_connections) == 0:
            #print('len(local_connections) == 0')
            return []

        i, maximum = max(local_connections, key = operator.itemgetter(1))
        #print('i: ', i, 'Max: ', maximum)

        if i == end_node:
            #print('reached end_node')
            return i
        else:
            visited.append(i)
            if not get_row_max(costs, i, visited.copy(), end_node):
                list[i] = 0
            else:
                return i
    #print('all zero')
    return []


def get_result(cost_map, end_node):
    total_cost = 0
    for i in cost_map[end_node - 1][1:]:
        if i > 0:
            total_cost += i

    return total_cost

data_list = read_file()
print('Data list:\n ', data_list)
all_nodes = np.concatenate([data_list[:, 0], data_list[:, 1]])
node_dict = Counter(all_nodes).keys()
node_number = len(node_dict)
print('Nodes: ', node_dict)
data_map = create_dictionary(data_list, list(node_dict))
print('\nData Map: ')
for l in data_map:
    print(l)
data_map = np.array(data_map)
start_node = min(data_map[:, 0])
last_node = max(np.array(data_map)[:, 0])
print('start: ', start_node, ' last: ', last_node)
#print('Is path possible: ', is_path_possible(data_map, [], start_node, last_node))
result = iteraction(data_map, start_node, last_node)
print('\n\n',result)
print('Resultado: ', get_result(result, last_node))
