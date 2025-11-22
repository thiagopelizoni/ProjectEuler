# Problem: https://projecteuler.net/problem=422

def main():
    M = 1000000007
    phi = M - 1
    n = 11 ** 14
    m = n - 2
    K = [[phi - 1, 1], [1, 0]]
    
    def mat_mult(A, B, mod):
        return [
            [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod,
             (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod],
            [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod,
             (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod]
        ]
    
    def mat_pow(mat, exp, mod):
        result = [[1, 0], [0, 1]]
        base = [row[:] for row in mat]
        
        while exp > 0:
            if exp % 2 == 1:
                result = mat_mult(result, base, mod)
            base = mat_mult(base, base, mod)
            exp //= 2
        
        return result
    
    pow_k = mat_pow(K, m, phi)
    
    p1 = (-2) % phi
    p2 = 1 % phi
    p_n = (pow_k[0][0] * p2 + pow_k[0][1] * p1) % phi
    
    q1 = 0 % phi
    q2 = (-1) % phi
    q_n = (pow_k[0][0] * q2 + pow_k[0][1] * q1) % phi
    
    s = 1
    neg_p = (phi - p_n) % phi
    
    exp_2_a = (2 * neg_p - 2) % phi
    term_2a = pow(2, exp_2_a, M)
    exp_3_a = (2 * q_n - 1) % phi
    term_3a = pow(3, exp_3_a, M)
    a = (s * (term_2a + term_3a)) % M
    
    exp_2_b = (neg_p - 2) % phi
    two_b = pow(2, exp_2_b, M)
    exp_3_b = (q_n - 1) % phi
    three_b = pow(3, exp_3_b, M)
    b = (two_b * three_b) % M
    
    exp_2_c = (2 * neg_p) % phi
    two_c = pow(2, exp_2_c, M)
    term_1c = (4 * two_c) % M
    exp_3_c = (2 * q_n) % phi
    three_c = pow(3, exp_3_c, M)
    term_2c = (3 * three_c) % M
    diff_c = (term_1c - term_2c) % M
    c = (s * diff_c) % M
    
    exp_2_d = neg_p % phi
    two_d = pow(2, exp_2_d, M)
    three_d = pow(3, q_n, M)
    d = (two_d * three_d) % M
    
    total = (a + b + c + d) % M
    print(total)


if __name__ == "__main__":
    main()