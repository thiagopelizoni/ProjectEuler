# Problem: https://projecteuler.net/problem=39
def right_triangle_solutions(p):
    solutions = 0
    for a in range(1, p // 3):
        for b in range(a, (p - a) // 2):
            c = p - a - b
            if a * a + b * b == c * c:
                solutions += 1
    return solutions

def most_solutions(limit):
    max_solutions = 0
    max_p = 0
    for p in range(2, limit + 1, 2):
        solutions = right_triangle_solutions(p)
        if solutions > max_solutions:
            max_solutions = solutions
            max_p = p
    return max_p

answer = most_solutions(1000)
print(answer)
