# Problem: https://projecteuler.net/problem=329
from fractions import Fraction
from math import sqrt
from tqdm import tqdm


def sieve(n):
    """Generate a boolean list indicating primes up to n."""
    if n < 2:
        return [False] * (n + 1)
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime


def get_neighbors(j, N=500):
    """Return list of (next_position, transition_prob) from j."""
    if j == 1:
        return [(2, Fraction(1))]
    elif j == N:
        return [(N - 1, Fraction(1))]
    else:
        half = Fraction(1, 2)
        return [(j - 1, half), (j + 1, half)]


def emit_prob(i, c, is_prime):
    """Emission probability of croak c at position i."""
    is_p = is_prime[i]
    if c == 'P':
        return Fraction(2, 3) if is_p else Fraction(1, 3)
    return Fraction(1, 3) if is_p else Fraction(2, 3)


def main():
    is_prime = sieve(500)
    seq = list('PPPPNNPPPNPPNPN')
    N = 500
    T = 15

    prev_dp = [Fraction(0)] * (N + 1)
    for i in range(1, N + 1):
        prev_dp[i] = Fraction(1, N) * emit_prob(i, seq[0], is_prime)

    for t in tqdm(range(1, T), desc='Computing probabilities'):
        curr_dp = [Fraction(0)] * (N + 1)
        for j in range(1, N + 1):
            p = prev_dp[j]
            if p == 0:
                continue
            for next_i, p_trans in get_neighbors(j):
                e = emit_prob(next_i, seq[t], is_prime)
                curr_dp[next_i] += p * p_trans * e
        prev_dp = curr_dp

    total_prob = sum(prev_dp[1:])
    num = total_prob.numerator
    den = total_prob.denominator
    print(f'{num}/{den}')


if __name__ == '__main__':
    main()