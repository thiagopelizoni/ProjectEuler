# Problem: https://projecteuler.net/problem=93
from itertools import permutations, product

def apply_operation(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b if b != 0 else None

def valid_expressions(digits):
    results = set()
    for perm in permutations(digits):
        for ops in product('+-*/', repeat=3):
            a, b, c, d = perm
            try:
                res1 = apply_operation(apply_operation(apply_operation(a, b, ops[0]), c, ops[1]), d, ops[2])
                res2 = apply_operation(apply_operation(a, apply_operation(b, c, ops[1]), ops[0]), d, ops[2])
                res3 = apply_operation(a, apply_operation(b, apply_operation(c, d, ops[2]), ops[1]), ops[0])
                res4 = apply_operation(apply_operation(a, b, ops[0]), apply_operation(c, d, ops[2]), ops[1])
                res5 = apply_operation(a, apply_operation(apply_operation(b, c, ops[1]), d, ops[2]), ops[0])
                for res in [res1, res2, res3, res4, res5]:
                    if res is not None and res == int(res) and res > 0:
                        results.add(int(res))
            except:
                pass
    return results

def find_longest_consecutive_set():
    longest_set = set()
    longest_digits = ()
    for digits in permutations(range(1, 10), 4):
        current_set = valid_expressions(digits)
        n = 1
        while n in current_set:
            n += 1
        if n - 1 > len(longest_set):
            longest_set = current_set
            longest_digits = digits
    return ''.join(map(str, longest_digits))

result = find_longest_consecutive_set()
print(result)
