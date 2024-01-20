# Problem: https://projecteuler.net/problem=41
def largest_pandigital_prime():
    for n in range(9, 0, -1):
        digits = ''.join(str(i) for i in range(1, n + 1))
        for p in sorted(permutations(digits), reverse=True):
            num = int(''.join(p))
            if is_prime(num):
                return num

answer = largest_pandigital_prime()
print(answer)
