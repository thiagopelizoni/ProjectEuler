# Problem: https://projecteuler.net/problem=66
from sympy import sqrt
from sympy.solvers.diophantine.diophantine import diop_DN

def compute_largest_x_for_pell(D_max):
    max_x_found = 0
    D_with_max_x = 0

    for D in range(2, D_max + 1):
        if sqrt(D).is_rational:
            continue

        try:
            minimal_solution = diop_DN(D, 1)[0]
            if minimal_solution[0] > max_x_found:
                max_x_found = minimal_solution[0]
                D_with_max_x = D
        except IndexError:
            continue

    return D_with_max_x

# Compute the largest x for Pell's equation with D up to 1000
answer = compute_largest_x_for_pell(1000)
print(answer)
