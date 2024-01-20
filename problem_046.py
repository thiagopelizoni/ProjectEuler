# Problem: https://projecteuler.net/problem=46
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def answer():
    n = 3
    while True:
        if not is_prime(n):
            goldbach_holds = False
            for i in range(1, n):
                if is_prime(i) and ((n - i) / 2)**0.5 == int(((n - i) / 2)**0.5):
                    goldbach_holds = True
                    break
            if not goldbach_holds:
                return n
        n += 2

print(answer())
