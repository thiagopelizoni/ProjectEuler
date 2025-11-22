# Problem: https://projecteuler.net/problem=290
from tqdm import tqdm

def sum_digits(num):
    s = 0
    while num > 0:
        s += num % 10
        num //= 10
    return s

def main():
    DIGITS = 18
    MAX_CARRY = 136
    MIN_DIFF = -200
    MAX_DIFF = 200
    OFFSET = -MIN_DIFF
    NUM_DIFF = MAX_DIFF - MIN_DIFF + 1
    NUM_CARRY = MAX_CARRY + 1
    dp = [[[0 for _ in range(NUM_DIFF)] for _ in range(NUM_CARRY)] for _ in range(DIGITS + 1)]
    dp[0][0][0 + OFFSET] = 1
    for pos in tqdm(range(DIGITS)):
        for carry in range(NUM_CARRY):
            for i in range(NUM_DIFF):
                if dp[pos][carry][i] == 0:
                    continue
                prev_diff = i - OFFSET
                for d in range(10):
                    temp = d * 137 + carry
                    m_dig = temp % 10
                    carry_next = temp // 10
                    diff_next = prev_diff + d - m_dig
                    i_next = diff_next + OFFSET
                    if 0 <= i_next < NUM_DIFF:
                        dp[pos + 1][carry_next][i_next] += dp[pos][carry][i]
    total = 0
    for carry in range(NUM_CARRY):
        for i in range(NUM_DIFF):
            if dp[DIGITS][carry][i] == 0:
                continue
            final_diff = i - OFFSET - sum_digits(carry)
            if final_diff == 0:
                total += dp[DIGITS][carry][i]
    print(total)

if __name__ == "__main__":
    main()