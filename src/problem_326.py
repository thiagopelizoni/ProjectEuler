# Problem: https://projecteuler.net/problem=326
from collections import Counter
from tqdm import tqdm

def formula_S(n: int) -> int:
    """Compute the exact prefix sum S_n = sum_{k=1}^n a_k."""
    if n <= 0:
        return 0
    p = n // 6
    rem = n % 6
    total = 9 * p * p - p
    if rem >= 1:
        total += 4 * p + 1
    if rem >= 2:
        total += 3 * p + 1
    if rem >= 3:
        total += p
    if rem >= 4:
        total += 6 * p + 3
    if rem >= 5:
        total += p
    return total


def main() -> None:
    """
    Purpose
    -------
    Solve Project Euler problem 326: compute f(10^12, 10^6), the number of subarrays
    with sum congruent to 0 modulo 10^6.

    Method / Math Rationale
    -----------------------
    The sequence a_n has closed-form expressions per n mod 6, leading to quadratic
    S_n = sum_{k=1}^n a_k. The residues S_k mod M are computed via S_k % M.
    The sequence of residues has period P = lcm(6, M) = 3*10^6, but with class-
    dependent shifts (0 or M/2) for positions based on k mod 6. Group positions by
    mod 6 into shifting (rems 0,1,3,4) and non-shifting (2,5) classes. Full periods
    contribute via scaled base counts, adjusted for parity-induced shifts in shifting
    classes. Remainder computed by direct shifted residues.

    Complexity
    ----------
    O(P + M) = O(10^6)

    References
    ----------
    https://projecteuler.net/problem=326
    """
    N = 10**12
    M = 10**6
    P = 3 * M
    q = N // P
    rem_len = N % P
    shift = M // 2
    class_count = [Counter() for _ in range(6)]
    for k in tqdm(range(1, P + 1), desc="Computing base counts"):
        rk = formula_S(k) % M
        rem_k = k % 6
        class_count[rem_k][rk] += 1
    shifting_base = Counter()
    for remm in [0, 1, 3, 4]:
        shifting_base += class_count[remm]
    non_shifting_base = Counter()
    for remm in [2, 5]:
        non_shifting_base += class_count[remm]
    rem_actual = Counter()
    q_mod2 = q % 2
    shifting_rems = {0, 1, 3, 4}
    for l in tqdm(range(1, rem_len + 1), desc="Computing remainder"):
        base_rk = formula_S(l) % M
        l_rem = l % 6
        is_shift = l_rem in shifting_rems
        added = shift if (q_mod2 == 1 and is_shift) else 0
        actual_rk = (base_rk + added) % M
        rem_actual[actual_rk] += 1
    total = 0
    num_un_m = (q + 1) // 2
    num_sh_m = q // 2
    for r in range(M):
        non_contrib = q * non_shifting_base[r]
        shift_un = num_un_m * shifting_base[r]
        shift_sh = num_sh_m * shifting_base[(r + shift) % M]
        full_contrib = non_contrib + shift_un + shift_sh
        add_contrib = rem_actual[r]
        fr = (1 if r == 0 else 0) + full_contrib + add_contrib
        total += fr * (fr - 1) // 2
    print(total)


if __name__ == "__main__":
    main()