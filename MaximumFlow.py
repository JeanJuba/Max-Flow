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
    while is_path_possible(cost_map, [].copy(), start_node, end_n):
        s_global = []
        i = 0
        connections = []
        visited = []
        last_valid = [0]
        while i + 1 != end_n:
            print('\ni: ', i)
            print('visited:', visited)
            s_local = []
            node = cost_map[i][0]
            row = cost_map[i]
            for index, cost in enumerate(row[1:]):
                #print('index: ', index,  ' cost: ', cost)
                if cost > 0 and index not in visited:
                    #print('added')
                    s_local.append([index+1, cost])
            print('s_local: ', s_local)
            if not s_local and last_valid[-1] != i:
                visited.append(i)
                i = last_valid[-1]
                connections.pop()
                s_global.pop()

            elif not s_local and last_valid[-1] == i:
                print('i: ', i)
                print('last_valid: ', last_valid)
                print('global: ', s_global)
                return cost_map
            else:
                print('s_local before: ', s_local)
                #remove_dead_ends(cost_map, s_local, visited.copy())
                if not s_local:
                    return cost_map
                print('s_local after: ', s_local)
                np_array_local = np.array(s_local)
                n, con_val = max(np_array_local, key=operator.itemgetter(1))
                print('nodo: ', n, 'max: ', con_val)
                s_global.append(con_val)
                connections.append([node, n])
                visited.append(i)
                last_valid.append(i)
                i = n - 1

        min_cost =  min(s_global)
        print('***min: ', min_cost)
        print('***connections: ', connections)
        update_connections(cost_map, connections, min_cost)
    print(cost_map)


def update_connections(cost_map, connections, value):
    old_cost = cost_map.copy()
    print('\nvalue: ', value)
    for con in connections:
        print('con: ', con)
        row = cost_map[con[0] - 1][1:]  #nodo
        print('1 - row before: ', row)
        row[con[1] - 1] = row[con[1] - 1] - value
        print('1 - row after:  ', row)
        row = cost_map[con[1] - 1][1:]  #nodo
        print('2 - row before: ', row)
        row[con[0] - 1] = row[con[0] - 1] + value
        print('2 - row after:  ', row)
    print('old cost map: \n', old_cost, '\n')
    print('updated cost_map:\n ', cost_map, '\n')


"Checks if this is possible or not to get from the first to the last node"
def is_path_possible(cost_map, visited, start_n, end_n):
    for row in cost_map[slice(start_n-1, end_n)]:
        visited.append(row[0])               #Add the node index to visited
        for n, i in enumerate(row[1:]):
           #print('\nnode: ', n+1)
           #print('cost: ', i)
           #print('visited: ', visited)

            if i > 0 and (n+1) not in visited: #Cost is greater than 0 and the node index was not visited
                #print('cost accepted: ', i)
                if (n+1) == end_n: #node index is equal to the end node
                    return True
                else:
                    if is_path_possible(cost_map, visited.copy(), start_n + n, end_n): #Checks starting from the node index where a connection was found
                        #print('true')
                        return True
    #print('false')
    return False


def remove_dead_ends(cost_map, s_local=[], visitados=[]):
    print('temp s_local: ', s_local)
    print('visitados: ', visitados)
    for index, max_pos in enumerate(s_local):
        i = max_pos[0] - 1
        s_connec = []
        print('index: ', i)
        for n, cost in enumerate(cost_map[i][1:]):
            if cost > 0 and n != i and n not in visitados:#custo maior q 0 e nao for ele mesmo
                s_connec.append([n + 1, cost])

        print('s_connect: ', s_connec)
        if i not in visitados:
            visitados.append(i)
        print('\n *** remove dead ends ***')
        if not s_connec or not remove_dead_ends(cost_map, s_connec, visitados):
            if len(s_local) > 0:
                print('index to remove: ', index)
                print(s_local)
                s_local.pop(index)
            return s_local

    return s_local


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
print(result)
print('Resultado: ', get_result(result, last_node))
