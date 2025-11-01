# Problem: https://projecteuler.net/problem=471
import math
from mpmath import mp, mpf, harmonic, quad, diff, ln, euler, bernoulli, nstr

def main():
    """
    Purpose
    -------
    Computes G(10**11) where G(n) is the sum over a=3 to n and b=1 to floor((a-1)/2) of r(a,b),
    with r(a,b) = b * (a - 2b) / (a - b). Outputs the result in scientific notation rounded
    to 10 significant digits. No parameters. Returns None, prints the result.

    Method / Math Rationale
    ------------------------
    Derives r(a,b) from examples and verifies with G(10). Reorders summation over b then a.
    Uses closed-form expressions for polynomial sums and sum k^2 H_k. For sum l^2 H_{n-l},
    employs Euler-Maclaurin formula with asymptotic expansion of harmonic numbers using
    mpmath for high-precision computation.

    Complexity
    ----------
    O(1) - fixed number of arithmetic operations and quadrature evaluations.

    References
    ----------
    https://projecteuler.net/problem=471
    """

    mp.dps = 40  # Extra precision for safety

    n = 10**11
    m = (n - 1) // 2
    nn = mpf(n)
    mm = mpf(m)

    # Compute the exact first part
    first = nn * mm * (mm + 1) / 2 - 2 * mm * (mm + 1) * (2 * mm + 1) / 6

    def S(ll):
        if ll == 0:
            return mpf(0)
        hl = harmonic(ll)
        p = ll * (ll + 1) * (2 * ll + 1) / 6
        return p * hl - p / 3 + ll * (ll + 1) / 4 - ll / 6

    s_mm = S(mm)

    # Now compute T = sum_{l=1}^m l^2 * H_{n-l} using Euler-Maclaurin
    def H_approx(z):
        if z <= 0:
            return mpf(0)
        res = ln(z) + euler + mpf(0.5) / z
        j = 1
        while True:
            b = bernoulli(2 * j)
            term = -b / (mpf(2 * j) * z ** (2 * j))
            if abs(term) < mp.power(10, -(mp.dps + 5)):
                break
            res += term
            j += 1
        return res

    def f(x):
        return mpf(x) ** 2 * H_approx(nn - mpf(x))

    # Use variable change u = x / nn, integral = nn**3 * int_{1/nn}^{mm/nn} u**2 * H_approx(nn * (1 - u)) du
    low_u = mpf(1) / nn
    high_u = mm / nn
    integ = nn ** 3 * quad(lambda u: mpf(u) ** 2 * H_approx(nn * (1 - mpf(u))), [low_u, high_u])

    f1 = f(1)
    fm = f(mm)

    # Euler-Maclaurin terms
    approx = integ + (f1 + fm) / 2

    # Add higher-order terms
    bs = [bernoulli(2), bernoulli(4), bernoulli(6), bernoulli(8), bernoulli(10)]
    facts = [2, 24, 720, 40320, 3628800]
    orders = [1, 3, 5, 7, 9]
    for i in range(len(bs)):
        b2k = bs[i]
        fact = mpf(facts[i])
        order = orders[i]
        term = (b2k / fact) * (diff(lambda x: f(x), mm, order) - diff(lambda x: f(x), mpf(1), order))
        approx += term

    T = approx

    # Compute G
    G = first + s_mm - T

    # Format to 10 significant digits in scientific notation with lowercase 'e'
    g_str = nstr(G, 10)
    if 'e' in g_str:
        mant, exp = g_str.split('e')
        exp = exp.replace('+', '')
        result = mant + 'e' + exp
    else:
        # For small numbers, convert manually        
        if G == 0:
            result = '0e0'
        else:
            exp = math.floor(math.log10(float(G)))
            mant = G / mpf(10)**exp
            mant_str = nstr(mant, 10)
            result = mant_str + 'e' + str(exp)

    print(result)

if __name__ == "__main__":
    main()