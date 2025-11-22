# Problem: https://projecteuler.net/problem=450
from fractions import Fraction
from math import gcd, lcm
import math
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def compute_mobius(n):
    mu = [0] * (n + 1)
    prime = [True] * (n + 1)
    mu[1] = 1
    for i in range(2, n + 1):
        if prime[i]:
            mu[i] = -1
            for j in range(i * 2, n + 1, i):
                prime[j] = False
                if (j // i) % i == 0:
                    mu[j] = 0
                else:
                    mu[j] = -mu[j // i]
    return mu

def compute_Tn_U_nm1(c, n):
    if n == 0:
        return Fraction(1), Fraction(0)
    T_prev = Fraction(1)
    T = c
    U_prev2 = Fraction(0)
    U_prev = Fraction(1)
    for _ in range(2, n + 1):
        T_new = 2 * c * T - T_prev
        U_new = 2 * c * U_prev - U_prev2
        T_prev = T
        T = T_new
        U_prev2 = U_prev
        U_prev = U_new
    return T, U_prev

def compute_base_contrib(arg):
    p, q, N = arg
    m = p * p + q * q
    if m == 0:
        return Fraction(0)
    c_b = Fraction(p * p - q * q, m)
    s_b = Fraction(2 * p * q, m)
    max_n = max(3, int(math.log(N + 1) / math.log(max(1.1, m))) + 10)
    total = Fraction(0)
    for t in range(1, max_n + 1):
        for s in range(t + 1, max_n + 1):
            if gcd(s, t) == 1:
                T_t, U_tm1 = compute_Tn_U_nm1(c_b, t)
                T_s, U_sm1 = compute_Tn_U_nm1(c_b, s)
                c_t = T_t
                c_s = T_s
                s_t = U_tm1 * s_b
                s_s = U_sm1 * s_b
                x_base = Fraction(s * c_t + t * c_s)
                y_base = Fraction(s * s_t - t * s_s)
                q_den = lcm(x_base.denominator, y_base.denominator)
                if q_den == 0:
                    continue
                st_sum = s + t
                max_k = N // (q_den * st_sum)
                if max_k <= 0:
                    continue
                point_sum = abs(x_base) + abs(y_base)
                mult = 2 if y_base != 0 else 1
                sum_k = max_k * (max_k + 1) // 2
                contrib = mult * point_sum * q_den * sum_k
                total += contrib
    return total

def compute_divisors(n):
    divisors = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            divisors[j].append(i)
    return divisors

def special_contrib(N, mu, base_type, divisors):
    total = 0
    for d in range(3, N + 1):
        k = (d - 1) // 2
        num = 0
        sum_t = 0
        for e in divisors[d]:
            fl = k // e
            num += mu[e] * fl
            sum_t += mu[e] * e * fl * (fl + 1) // 2
        M = N // d
        contrib = 0
        if base_type == 'one':
            contrib = num * d * M * (M + 1) // 2
        elif base_type == 'two':
            if d % 2 == 0:
                contrib = num * d * M * (M + 1) // 2
            else:
                contrib = (d * num - 2 * sum_t) * M * (M + 1) // 2
        elif base_type == 'three':
            if d % 4 == 2:
                contrib = (d * num - 2 * sum_t) * M * (M + 1) // 2
            else:
                contrib = num * d * M * (M + 1) // 2
            contrib *= 2
        total += contrib
    return total

def main():
    N = 1000000
    mu = compute_mobius(N)
    divisors = compute_divisors(N)
    total = Fraction(0)
    total += special_contrib(N, mu, 'one', divisors)
    total += special_contrib(N, mu, 'two', divisors)
    total += special_contrib(N, mu, 'three', divisors)
    max_pq = 600
    bases = []
    for p in range(0, max_pq + 1):
        for q in range(0, max_pq + 1):
            m = p * p + q * q
            if m > 2 and gcd(p, q) == 1:
                bases.append((p, q))
    args_list = [(p, q, N) for p, q in bases]
    with ProcessPoolExecutor() as executor:
        for result in tqdm(executor.map(compute_base_contrib, args_list), total=len(args_list)):
            total += result
    print(int(total))

if __name__ == "__main__":
    main()