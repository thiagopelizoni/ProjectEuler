# Problem: https://projecteuler.net/problem=101
from sympy import symbols, Matrix

def u(n):
    return sum((-n)**k for k in range(11))

def solve_poly(matrix, y_values):
    coeffs = Matrix(matrix).inv() * Matrix(y_values)
    return coeffs

def fit_op(seq, k):
    matrix = [[n**i for i in range(k)] for n in range(1, k+1)]
    y_values = seq[:k]
    coeffs = solve_poly(matrix, y_values)
    x = symbols('x')
    return sum(coeffs[i] * x**i for i in range(k))

def find_bop(seq):
    total_sum = 0
    for k in range(1, len(seq)):
        op = fit_op(seq, k)
        bop_k = op.subs(symbols('x'), k+1)
        total_sum += bop_k
    return total_sum

if __name__ == "__main__":
    seq = [u(n) for n in range(1, 12)]
    answer = find_bop(seq)
    print(answer)
