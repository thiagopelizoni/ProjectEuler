# Problem: https://projecteuler.net/problem=281
from math import factorial
from typing import List
from tqdm import tqdm

def get_divisors(n: int) -> List[int]:
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    divisors.sort()
    return divisors

def totient(n: int) -> int:
    if n == 0:
        return 0
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            result -= result // i
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        result -= result // n
    return result

def compute_f(m: int, n: int) -> int:
    k = m * n
    divisors = get_divisors(n)
    total = 0
    for t in divisors:
        phi = totient(n // t)
        fact_mt = factorial(m * t)
        fact_t = factorial(t)
        term = phi * (fact_mt // (fact_t ** m))
        total += term
    f = total // k
    return f

def main() -> None:
    """
    Purpose
    Solves Project Euler problem 281: computes the sum of all f(m, n) where f(m, n) <= 10^15, and f(m, n) is the number of ways to place m distinct toppings each on exactly n slices of a pizza divided into m*n equal slices, considering arrangements distinct under reflection but identical under rotation.

    Method / Math Rationale
    Uses Burnside's lemma on the cyclic group to derive f(m, n) = (1 / (m * n)) * sum_{t divides n} phi(n / t) * ((m * t)! / (t!)^m). Loops over m starting from 2 and increases n from 1 until f(m, n) exceeds 10^15, adding valid f(m, n) to the total sum.

    Complexity
    O(1) effectively, as loops are bounded by small constants (m < 25, n < 100).

    References
    https://projecteuler.net/problem=281
    """
    total = 0
    for m in tqdm(range(2, 25)):
        n = 1
        while n < 100:
            f = compute_f(m, n)
            if f > 10**15:
                break
            total += f
            n += 1
    print(total)

if __name__ == "__main__":
    main()