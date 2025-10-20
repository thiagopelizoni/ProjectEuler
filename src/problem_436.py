# Problem: https://projecteuler.net/problem=436
import sympy as sp

def main():
    """
    Purpose
    -------
    Computes the probability that the second player wins in the unfair wager game
    described in Project Euler problem 436 and prints it rounded to 10 decimal
    places in the form 0.abcdefghij.
      
    Method / Math Rationale
    -----------------------
    Derives the PDFs: p_x(z) = e - exp(1 - z) for the first player's last number.
    p_y(y) = integrate_{1-y to 1} exp(t) * (e - 1 - t) dt = exp(1) * (e - 1) -
    exp(1 - y) * (e - 1 + y)
    CDF_x(y) = e * y + exp(1 - y) - e
    The probability is integrate_0^1 p_y(y) * CDF_x(y) dy, computed symbolically
    with sympy for exactness, then evaluated numerically.
    
    Complexity
    ----------
    Time: O(1)
    Space: O(1)
    
    References
    ----------
    https://projecteuler.net/problem=436
    """
    e = sp.E
    y = sp.symbols('y')
    F = e * y + sp.exp(1 - y) - e
    Q = e * (e - 1) - sp.exp(1 - y) * (e - 1 + y)
    integrand = Q * F
    ans = sp.integrate(integrand, (y, 0, 1))
    prob = ans.evalf(12)
    print(f"{prob:.10f}")

if __name__ == "__main__":
    main()