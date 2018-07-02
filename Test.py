import operator
import numpy as np

def changer(list = []):
    list[:] = [x * 10 for x in list]
    print('List inside method: ', list)


def find_max(cost_map, i, visited=[]):
    row = cost_map[i]
    s_local = []
    for index, cost in enumerate(row[1:]):
        if cost > 0 and index not in visited:
            s_local.append([index + 1, cost])
    visited.append(i)
    print(s_local)
    remove_dead_ends(cost_map, s_local, visited)
    print('s_local final :  ', s_local)


def remove_dead_ends(cost_map, s_local=[], visitados=[]):
    print('\ntemp s_local: ', s_local)
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

        if not s_connec or not remove_dead_ends(cost_map, s_connec, visitados):
            if len(s_local) > 0:
                print('index to remove: ', index)
                print(s_local)
                s_local.pop(index)
            return s_local

    return s_local


def is_dead_end(costs, node, visited, end_node ):
    print('\nNode: ', node)
    visited.append(node)
    print('Visited: ', visited)
    local_connections = []
    #dead_end = True
    list = np.array(costs[node][1:].copy())
    print('list: ', list)
    while np.any(list):
        local_connections = []
        for index, cost in enumerate(list):
            if cost > 0 and index not in visited:
                local_connections.append([index, cost])

        print('Local connections: ', local_connections)
        if len(local_connections) == 0:
            print('len(local_connections) == 0')
            return []

        i, maximum = max(local_connections, key = operator.itemgetter(1))
        print('i: ', i, 'Max: ', maximum)

        if i == end_node:
            print('reached end_node')
            return i
        else:
            visited.append(i)
            if not is_dead_end(costs, i, visited.copy(), end_node):
                list[i] = 0
            else:
                return i
    print('all zero')
    return []

'''cost = \
[[ 1, 0,  3,  2, 1, 0],
 [ 2, 0,  0,  1, 0, 0],
 [ 3, 0,  3,  0, 2, 1],
 [ 4, 0,  5,  0, 0, 0],
 [ 5, 0,  0,  0, 0, 0]]'''

cost = [[1, 0, 8, 0, 0, 4],
        [2, 0, 0, 10, 2, 6],
        [3, 14, 5, 0, 9, 1],
        [4, 0, 11, 7, 0, 0],
        [5, 0, 0, 9, 5, 0]]

print(is_dead_end(cost, 2, [0, 1], 4))

#print('cost: ', cost)

