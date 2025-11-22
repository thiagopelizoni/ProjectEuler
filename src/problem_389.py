# Problem: https://projecteuler.net/problem=389
from fractions import Fraction

def get_mean_var(sides):
    return Fraction(sides + 1, 2), Fraction(sides**2 - 1, 12)

def main():
    m_t, v_t = get_mean_var(4)
    m6, v6 = get_mean_var(6)
    m_c = m6 * m_t
    v_c = m6**2 * v_t + v6 * m_t
    m8, v8 = get_mean_var(8)
    m_o = m8 * m_c
    v_o = m8**2 * v_c + v8 * m_c
    m12, v12 = get_mean_var(12)
    m_d = m12 * m_o
    v_d = m12**2 * v_o + v12 * m_o
    m20, v20 = get_mean_var(20)
    v_i = m20**2 * v_d + v20 * m_d
    print("{:.4f}".format(float(v_i)))

if __name__ == "__main__":
    main()