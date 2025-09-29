# Problem: https://projecteuler.net/problem=371
from decimal import Decimal, getcontext

getcontext().prec = 20

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 371 by computing the expected number of
    license plates needed until two are seen whose three-digit numbers sum
    to 1000.

    Method / Math Rationale
    -----------------------
    Models the problem using dynamic programming. States are defined by the
    number of "open" complementary pairs (where one side has been seen but
    not the other) and whether the number 500 has been seen once. Computes
    the expected additional plates needed from each state, working backwards
    from the maximum number of open pairs (499) to zero.

    Complexity
    ----------
    O(1) time and space, as the number of states is fixed at 500.

    References
    ----------
    https://projecteuler.net/problem=371
    """
    num_plates = 1000
    max_have = num_plates // 2 - 1  # 499
    plates = Decimal(num_plates)
    prob_zero = Decimal(1) / plates
    prob_500 = Decimal(1) / plates

    have_500 = [Decimal(0)] * (max_have + 1)
    no_500 = [Decimal(0)] * (max_have + 1)

    # Base case for max_have (499)
    prob_duplicate = Decimal(max_have) / plates
    prob_unchanged = prob_duplicate + prob_zero
    have_500[max_have] = Decimal(1) / (Decimal(1) - prob_unchanged)
    no_500[max_have] = (Decimal(1) + prob_500 * have_500[max_have]) / (Decimal(1) - prob_unchanged)

    # Fill the DP tables backwards
    for have in range(max_have - 1, -1, -1):
        num_new = plates - Decimal(2 * have) - Decimal(2)
        prob_new = num_new / plates
        prob_duplicate = Decimal(have) / plates
        prob_unchanged = prob_duplicate + prob_zero

        have_500[have] = (Decimal(1) + prob_new * have_500[have + 1]) / (Decimal(1) - prob_unchanged)
        no_500[have] = (Decimal(1) + prob_500 * have_500[have] + prob_new * no_500[have + 1]) / (Decimal(1) - prob_unchanged)

    # The answer is the expected value starting from 0 open pairs and no 500 seen
    print(f"{no_500[0]:.8f}")

if __name__ == "__main__":
    main()