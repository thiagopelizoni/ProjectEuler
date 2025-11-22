# Problem: https://projecteuler.net/problem=375
from tqdm import tqdm

def main():
    MOD = 50515093
    S0 = 290797
    N = 2000000000
    S = (S0 * S0) % MOD  # S1
    A = [S]
    S = (S * S) % MOD  # S2
    for _ in tqdm(range(MOD - 1)):
        A.append(S)
        S = (S * S) % MOD
        if S == A[0]:
            break
    P = len(A)
    Q = N // P
    R = N % P
    min_v = min(A)
    p_min = A.index(min_v)

    # Compute periodic left_span (distance to nearest strict < left, or None if infinite)
    Rev = A[::-1]
    B = Rev + Rev
    nB = len(B)
    right_left = [nB] * nB
    stack = []
    for i in range(nB - 1, -1, -1):
        while stack and B[stack[-1]] >= B[i]:
            stack.pop()
        if stack:
            right_left[i] = stack[-1]
        stack.append(i)
    left_span = [0] * P
    for r in range(P):
        if right_left[r] == nB:
            left_span[P - 1 - r] = None
        else:
            left_span[P - 1 - r] = right_left[r] - r

    # Compute periodic right_span (distance to nearest <= right, or None if infinite)
    B = A + A
    nB = len(B)
    right_right = [nB] * nB
    stack = []
    for i in range(nB - 1, -1, -1):
        while stack and B[stack[-1]] > B[i]:
            stack.pop()
        if stack:
            right_right[i] = stack[-1]
        stack.append(i)
    right_span = [0] * P
    for p in range(P):
        if right_right[p] == nB:
            right_span[p] = None
        else:
            right_span[p] = right_right[p] - p

    total = 0

    # Handle non-min positions
    for p in range(P):
        if p == p_min:
            continue
        v = A[p]
        l_per = left_span[p]
        r_per = right_span[p]
        Mp = Q + (1 if p < R else 0)
        if Mp == 0:
            continue
        # First
        l_first = min(l_per, p + 1)
        r_first = r_per
        total += v * l_first * r_first
        if Mp > 1:
            # Last
            k_last = Mp - 1
            pos_last = k_last * P + p
            l_last = l_per
            r_last = min(r_per, N - pos_last)
            total += v * l_last * r_last
            # Middles
            if Mp > 2:
                num_mid = Mp - 2
                total += v * l_per * r_per * num_mid

    # Handle min positions
    Mp = Q + (1 if p_min < R else 0)
    if Mp == 0:
        print(total)
        return
    K = Mp - 1
    offset = p_min + 1
    if K >= 0:
        sum_k = K * (K - 1) // 2
        part = min_v * P * (P * sum_k + offset * K)
        total += part
    # Last
    pos_last = (Mp - 1) * P + p_min
    l_last = pos_last + 1
    r_last = N - pos_last
    total += min_v * l_last * r_last
    print(total)

if __name__ == "__main__":
    main()