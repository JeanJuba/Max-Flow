import operator

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
    local_connections = []
    dead_end = True
    list = costs[node][1:].copy()

    while len(list) > 0:

        for index, cost in enumerate(list):
            if cost > 0 and index not in visited:
                local_connections.append([index, cost])

        print('Local connections: ', local_connections)
        if len(local_connections) == 0:
            return True

        i, maximum = max(local_connections, key = operator.itemgetter(1))
        print('i: ', i, 'Max: ', maximum)

        if i == end_node:
            return False
        else:
            visited.append(node)
            if not is_dead_end(costs, i, visited.copy(), end_node):
                return False;
            else:
                n = visited.pop(-1)
                print('n: ', n)
                print('before pop: ', list)
                list.pop(n)
                print('after pop: ', list)

    return True

cost = \
[[ 1, 0,  3,  2],
 [ 2, 0,  0,  0],
 [ 3, 0,  0,  1]]

print(is_dead_end(cost, 0, [0], 2))