# Problem: https://projecteuler.net/problem=334
def sum_squares(a, b):
    def sum_to(n):
        if n < 0:
            return 0
        return n * (n + 1) * (2 * n + 1) // 6

    if a > b:
        return 0
    if a >= 0:
        return sum_to(b) - sum_to(a - 1)
    if b < 0:
        return sum_to(-a) - sum_to(-b - 1)
    # a < 0 <= b
    return sum_to(-a) + sum_to(b)

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 334 by computing the number of moves required to finish the bean spilling game with 1500 adjacent bowls.

    Method / Math Rationale
    -----------------------
    Generate the sequence b_i using the given recursive definition.
    Compute S = sum b_i and M = sum i * b_i.
    Determine if consecutive positions can be used based on whether the starting position L is integer.
    If not, use an interval of length S+1 and exclude one position to achieve the correct sum M.
    Compute sum of squares for the positions in the final configuration f and initial c.
    The number of moves is (sum j^2 f_j - sum j^2 c_j) // 2.

    Complexity
    ----------
    Time complexity: O(N) for N=1500 bowls.
    Space complexity: O(N) for storing b_i.

    References
    ----------
    https://projecteuler.net/problem=334
    """
    t = 123456
    b = []
    for _ in range(1500):
        if t % 2 == 0:
            t = t // 2
        else:
            t = t // 2 ^ 926252
        b.append(t % 2048 + 1)

    S = 0
    M = 0
    sum_j2_c = 0
    for i in range(1, 1501):
        bi = b[i - 1]
        S += bi
        M += bi * i
        sum_j2_c += bi * i * i

    # Check if consecutive
    consecutive = False
    L = 0
    if S != 0 and (2 * M) % S == 0:
        temp = (2 * M // S) - S + 1
        if temp % 2 == 0:
            L = temp // 2
            R = L + S - 1
            consecutive = True

    if not consecutive:
        m = M / S
        ideal_L = m - S / 2
        L = round(ideal_L)
        R = L + S
        length = S + 1
        sum_interval = length * (L + R) // 2
        excluded = sum_interval - M
        if not (L <= excluded <= R):
            if ideal_L < L:
                L -= 1
            else:
                L += 1
            R = L + S
            sum_interval = length * (L + R) // 2
            excluded = sum_interval - M
        sum_j2_f = sum_squares(L, R) - excluded * excluded
    else:
        sum_j2_f = sum_squares(L, R)

    answer = (sum_j2_f - sum_j2_c) // 2
    print(answer)

if __name__ == "__main__":
    main()