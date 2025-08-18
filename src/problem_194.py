# Problem: https://projecteuler.net/problem=194
A = 25
B = 75
C = 1984
MODULUS = 100000000
unit_edges = [[6, 7], [1, 2], [1, 3], [1, 6], [2, 3], [2, 7], [3, 4], [4, 5], [5, 6], [5, 7]]
vertex_colors = [0] * 8
unit_a_color_ways = 0
unit_b_color_ways = 0

def is_proper_coloring_from(starting_edge_index):
    for i in range(starting_edge_index, 10):
        u = unit_edges[i][0]
        v = unit_edges[i][1]
        if vertex_colors[u] == vertex_colors[v]:
            return False
    return True

def explore_color_assignments(current_vertex, num_colors):
    global unit_a_color_ways
    global unit_b_color_ways
    if current_vertex == 0:
        color_used = [False] * (num_colors + 1)
        for j in range(1, 8):
            if vertex_colors[j] <= num_colors:
                color_used[vertex_colors[j]] = True
        if all(color_used[i] for i in range(1, num_colors + 1)):
            additional_color_ways = 1
            if num_colors > 1:
                for i in range(2, num_colors):
                    additional_color_ways = additional_color_ways * (C - i) // (i - 1)
            if is_proper_coloring_from(0):
                unit_a_color_ways = (unit_a_color_ways + additional_color_ways) % MODULUS
            if is_proper_coloring_from(1):
                unit_b_color_ways = (unit_b_color_ways + additional_color_ways) % MODULUS
        return
    if current_vertex == 1 or current_vertex == 6:
        explore_color_assignments(current_vertex - 1, num_colors)
        return
    for i in range(1, num_colors + 1):
        vertex_colors[current_vertex] = i
        explore_color_assignments(current_vertex - 1, num_colors)

vertex_colors[1] = 1
vertex_colors[6] = 2
for i in range(1, 8):
    explore_color_assignments(7, i)

binomial = [[0] * (A + B + 10) for _ in range(A + B + 10)]
for i in range(A + B + 1):
    for j in range(i + 1):
        if j == 0 or j == i:
            binomial[i][j] = 1
        else:
            binomial[i][j] = (binomial[i - 1][j - 1] + binomial[i - 1][j]) % MODULUS

final_result = binomial[A + B][B]
for i in range(1, A + 1):
    final_result = final_result * unit_a_color_ways % MODULUS
for i in range(1, B + 1):
    final_result = final_result * unit_b_color_ways % MODULUS
final_result = final_result * C % MODULUS
final_result = final_result * (C - 1) % MODULUS
print(final_result)