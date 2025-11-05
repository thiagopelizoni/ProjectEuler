# Problem: https://projecteuler.net/problem=477
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 477, computing the score F(10^8) of the first player in the number
    sequence game under optimal play.

    Method / Math Rationale
    ----------------------
    Generates the sequence s_i where s_1 = 0, s_{i+1} = (s_i^2 + 45) mod 1000000007.
    Uses an O(N) algorithm based on fusion principle to reduce the array by fusing triples where the
    middle value is at least as large as both neighbors.
    Computes the game value 'val' as the alternating sum of the sorted (descending) reduced array values.
    The first player's score F(N) is (total sum + val) // 2.

    Complexity
    ----------
    O(N log N) in worst case due to sorting the reduced array (reduced size up to N); in practice closer
    to O(N) for this sequence.

    References
    ----------
    https://projecteuler.net/problem=477
    An Optimal Algorithm for Calculating the Profit in the Coins in a Row Game by Tomasz Idziaszek.
    """
    MOD = 1000000007
    N = 10**8
    s = [0] * N
    current = 0
    total_sum = 0
    for i in tqdm(range(N)):
        s[i] = current
        total_sum += current
        current = (current * current + 45) % MOD

    sc = []
    for v in s:
        sc.append(v)
        while len(sc) >= 3 and sc[-3] <= sc[-2] and sc[-2] >= sc[-1]:
            new_v = sc[-3] - sc[-2] + sc[-1]
            sc.pop()
            sc.pop()
            sc[-1] = new_v

    sorted_sc = sorted(sc, reverse=True)
    val = 0
    sign = 1
    for x in sorted_sc:
        val += sign * x
        sign = -sign

    result = (total_sum + val) // 2
    print(result)

if __name__ == "__main__":
    main()