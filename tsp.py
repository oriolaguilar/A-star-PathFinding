import sys

def tsp_algorithm(matrix):
    """Traveling Salesman Person Algorithm, Hungarian Method """
    upperbound = sys.maxsize
    all_nodes = [i for i in range(len(matrix))]
    node = ([0], reduce_matrix(matrix), matrix)
    stack = []
    shortest_path = []
    stack.append(node)
    while stack:
        node = select_smallest_child(stack)
        if len(remaining_nodes(all_nodes, node[0])) == 0:
            upperbound = min(upperbound, node[1])
            shortest_path = node[0]
        else:
            if node[1] < upperbound:
                for child in remaining_nodes(all_nodes, node[0]):
                    new_matrix = new_matrix_generator(node[0][-1], child, node[2])
                    new_matrix[node[0][-1]][node[0][0]] = sys.maxsize
                    aux2 = reduce_matrix(new_matrix)
                    new_cost = node[1] + node[2][node[0][-1]][child] + aux2
                    stack.append((node[0]+[child], new_cost, new_matrix))
    return shortest_path+[0]


def select_smallest_child(stack):
    index = 0
    minimum = sys.maxsize
    for i, el in enumerate(stack):
        if el[1] < minimum:
            minimum = el[1]
            index = i
    return stack.pop(index)


def new_matrix_generator(row, column, matrix):
    matrix_ret = [[0] * len(matrix) for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == row or j == column:
                matrix_ret[i][j] = sys.maxsize
            else:
                matrix_ret[i][j] = matrix[i][j]
    return matrix_ret

def remaining_nodes(nodes, already):
    ret = []
    for node in nodes:
        if node not in already:
            ret.append(node)
    return ret

def reduce_matrix(matrix):
    minimums = []
    for row in matrix:
        aux = sys.maxsize
        for pos in row:
            aux = min(pos, aux)
        minimums.append(aux if aux != sys.maxsize else 0)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != sys.maxsize:
                matrix[i][j] -= minimums[i]

    horizontal_sum = sum(minimums)
    minimums = []
    for i in range(len(matrix)):
        aux = sys.maxsize
        for j in range(len(matrix[0])):
            aux = min(aux, matrix[j][i])
        minimums.append(aux if aux != sys.maxsize else 0)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[j][i] != sys.maxsize:
                matrix[j][i] -= minimums[i]

    return sum(minimums) + horizontal_sum