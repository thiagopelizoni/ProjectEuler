# Problem: https://projecteuler.net/problem=394
from decimal import Decimal, getcontext
import math

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 394: compute E(40), the expected number of procedure repeats
    when eating pie with F=1/40, rounded to 10 decimal places.
    No parameters.
    Prints the result.

    Method / Math Rationale
    -----------------------
    Models the process as a recursive expectation e(s), where s is the current remaining fraction.
    Leads to the integral equation e(s) = 1 + (2/s^2) int_F^s (s - r) e(r) dr for s >= F=1/x,
    e(s)=0 for s < F.
    Differentiating twice yields the DE s^2 e''(s) + 4 s e'(s) - 2 = 0.
    General solution e(s) = A + B s^{-3} + (2/3) ln s.
    Boundary conditions e(F)=1 and e'(F)=0 determine A = 7/9 - (2/3) ln F,
    B = (2/9) F^3.
    Thus E(x) = e(1) = 7/9 + (2/3) ln x + (2/9) x^{-3}.

    Complexity

    Time: O(1)
    Space: O(1)

    References
    ----------
    https://projecteuler.net/problem=394
    """
    getcontext().prec = 20
    x = Decimal(40)
    ln_x = Decimal(math.log(40))
    term1 = Decimal(7) / Decimal(9)
    term2 = (Decimal(2) / Decimal(3)) * ln_x
    term3 = (Decimal(2) / Decimal(9)) / (x ** 3)
    result = term1 + term2 + term3
    print(f"{result:.10f}")

if __name__ == "__main__":
    main()