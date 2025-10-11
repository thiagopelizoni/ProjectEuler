# Problem: https://projecteuler.net/problem=412
import os
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def partial_prod(start, end, mod):
    res = 1
    for i in range(start, end + 1):
        res = (res * i) % mod
    return res

def row_prod(i, m, n, mod):
    l = m - n
    lam_i = m if i <= l else l
    res = 1
    for j in range(1, lam_i + 1):
        lam_j = m if j <= l else l
        h = lam_i + lam_j - i - j + 1
        res = (res * h) % mod
    return res

def main():
    r"""
    Purpose
    -------
    Solves Project Euler problem 412 by computing LC(10000, 5000) mod 76543217, where LC(m, n) is the number of valid
    numberings of the gnomon L(m, n).

    Method / Math Rationale
    -----------------------
    LC(m, n) is the number of standard Young tableaux of shape (m^{m-n}, (m-n)^n), given by the hook-length formula:
    (m^2 - n^2)! / \prod_{(i,j) \in \lambda} h_{i,j}, where h_{i,j} = \lambda_i + \lambda_j - i - j + 1 since the partition
    is self-conjugate. Computes the factorial and the product of hook lengths modulo p using parallel processing for
    efficiency, then inverts the product.

    Complexity
    ----------
    Time: O(m^2 - n^2 / cpus), space: O(1).

    References
    ----------
    https://projecteuler.net/problem=412
    """
    m = 10000
    n = 5000
    p = 76543217
    k = m * m - n * n

    # Compute k! % p using parallel processing
    num_processes = os.cpu_count()
    chunk_size = k // num_processes
    futures_fac = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for idx in range(num_processes):
            start = idx * chunk_size + 1
            end = (idx + 1) * chunk_size if idx < num_processes - 1 else k
            if start <= end:
                futures_fac.append(executor.submit(partial_prod, start, end, p))

    fac_k = 1
    for future in futures_fac:
        fac_k = fac_k * future.result() % p

    # Compute prod_h % p using parallel processing over rows
    futures_rows = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for i in range(1, m + 1):
            futures_rows.append(executor.submit(row_prod, i, m, n, p))

    prod_h = 1
    for future in tqdm(futures_rows):
        prod_h = prod_h * future.result() % p

    # inv_prod_h = prod_h^{p-2} % p
    inv_prod_h = pow(prod_h, p - 2, p)

    # result = fac_k * inv_prod_h % p
    result = fac_k * inv_prod_h % p

    print(result)

if __name__ == "__main__":
    main()