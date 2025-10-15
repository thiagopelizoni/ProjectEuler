# Problem: https://projecteuler.net/problem=420
import math
from tqdm import tqdm
import concurrent.futures
import numba


@numba.jit(nopython=True)
def num_divisors(n):
    if n <= 0:
        return 0
    count = 0
    sq = int(math.sqrt(n)) + 1
    for i in range(1, sq):
        if n % i == 0:
            count += 1
            if i != n // i:
                count += 1
    return count


def process_n(n, N):
    count = 0
    is_even = n % 2 == 0
    max_m_sq = 2 * (N - 1) - n**2

    if max_m_sq <= 0:
        return 0

    max_m = int(math.sqrt(max_m_sq)) + n + 1

    for mm in range(n + 2, max_m + 1, 2):
        m = mm
        if m % 2 != n % 2:
            continue

        tau = (m**2 + n**2) // 2
        if tau >= N:
            break

        k = (m**2 - n**2) // 4
        g = math.gcd(m, n)

        if (2 * k) % g != 0:
            continue

        m1 = m // g
        n1 = n // g
        k1 = (2 * k) // g

        if n1 > 1:
            inv = pow(m1, -1, n1)
            x0 = (k1 * inv) % n1
        else:
            x0 = 0

        step = n1
        t_min = math.ceil((1 - x0) / step)
        t_max = math.floor((m - 1 - x0) / step)
        v = n1
        v2 = v * v

        for t in range(t_min, t_max + 1):
            x = x0 + step * t

            if x < 1 or x > m - 1:
                continue

            f = x * (m - x) - k

            if f <= 0 or f % v2 != 0:
                continue

            f_prime = f // v2
            e = (m * x - 2 * k) // n

            if e < 1 or e > n - 1:
                continue

            count += num_divisors(f_prime)

    return count


def main():
    """
    Purpose
    -------
    Computes F(N) for N=10^7, the number of 2x2 positive integer matrices with
    trace less than N that can be expressed as the square of a positive integer
    matrix in two different ways.

    Method / Math Rationale

    Parameterizes the two square roots R and S with traces m and n, det k and -k,
    with m^2 - n^2 =4k, tau = (m^2 + n^2)/2. Enumerates pairs m > n same parity,
    computes k, then finds congruent x for the top left of R, checks if f = x(m-x)-k
    divisible by v^2 where v=n/gcd(m,n), then adds the number of divisors of f/v^2
    if the conditions hold.

    Complexity
    ----------
    O(sqrt(N)^3) roughly, optimized with congruence to reduce inner loops, using
    Numba and parallel processing.

    References
    ----------
    https://projecteuler.net/problem=420
    https://math.stackexchange.com/questions/344148/project-euler-420
    https://en.wikipedia.org/wiki/Square_root_of_a_2_by_2_matrix
    """
    N = 10000000
    max_n = int(math.sqrt(2 * (N - 1))) + 1
    ns = list(range(2, max_n + 1))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_n, nn, N) for nn in ns]
        total = 0
        for future in tqdm(concurrent.futures.as_completed(futures)):
            total += future.result()

    print(total)


if __name__ == "__main__":
    main()