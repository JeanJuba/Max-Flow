def changer(list = []):
    list[:] = [x * 10 for x in list]
    print('List inside method: ', list)

'''a = [x * 2 for x in [1,2,3,4]]
print('List before method: ', a)
changer(a)
print('List after method: ', a)'''


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


cost = [[ 1,  0,  7,  0,  0,  4],
 [ 2, 1,  0,  9,  2,  6],
 [ 3, 14,  6,  0,  9,  0],
 [ 4,  0, 11,  7,  0,  0],
 [ 5,  0,  0, 10,  5,  0]]

find_max(cost, 1, [0])