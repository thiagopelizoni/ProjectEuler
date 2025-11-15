# Problem: https://projecteuler.net/problem=504
import math
import os
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from tqdm import tqdm

def build_square_lookup(max_interior, use_numpy):
    limit_sq = math.isqrt(max_interior)
    if use_numpy and np is not None:
        lookup = np.zeros(max_interior + 1, dtype=bool)
        for value in range(1, limit_sq + 1):
            lookup[value * value] = True
        return lookup
    lookup = [False] * (max_interior + 1)
    for value in range(1, limit_sq + 1):
        lookup[value * value] = True
    return lookup


def precompute_gcd_table_python(limit):
    table = [[0] * (limit + 1) for _ in range(limit + 1)]
    for x in range(1, limit + 1):
        row = table[x]
        for y in range(1, limit + 1):
            row[y] = math.gcd(x, y)
    return table


def count_quadrilaterals_vectorized(limit, is_square):
    if np is None:
        raise RuntimeError("NumPy is required for the vectorized implementation.")
    values = np.arange(1, limit + 1, dtype=np.int64)
    values_col = values.reshape(limit, 1)
    values_row = values.reshape(1, limit)
    gcd_table = np.gcd(values_col, values_row)
    gcd_cd = gcd_table
    total = 0
    for a_index in tqdm(
        range(limit),
        desc="a",
        unit="a",
        leave=False,
    ):
        a_value = a_index + 1
        a_plus_c = values_col + a_value
        g_ad_row = gcd_table[a_index, :].reshape(1, limit)
        for b_index in range(limit):
            b_value = b_index + 1
            b_plus_d = values_row + b_value
            g_ab = int(gcd_table[a_index, b_index])
            g_bc_col = gcd_table[b_index, :].reshape(limit, 1)
            rectangle = a_plus_c * b_plus_d
            boundary = g_ab + g_bc_col + g_ad_row + gcd_cd
            interior = (rectangle - boundary) // 2 + 1
            mask = is_square[interior]
            total += int(mask.sum())
    return total


def pure_python_worker(args):
    limit, a_start, a_end, is_square, gcd_table = args
    total = 0
    for a in range(a_start, a_end):
        for b in range(1, limit + 1):
            g_ab = gcd_table[a][b]
            for c in range(1, limit + 1):
                ac_sum = a + c
                g_bc = gcd_table[b][c]
                for d in range(1, limit + 1):
                    rectangle = ac_sum * (b + d)
                    g_cd = gcd_table[c][d]
                    g_ad = gcd_table[a][d]
                    boundary = g_ab + g_bc + g_ad + g_cd
                    interior = (rectangle - boundary) // 2 + 1
                    if is_square[interior]:
                        total += 1
    return total


def count_quadrilaterals_pure_python_sequential(limit, is_square, gcd_table):
    total = 0
    for a in tqdm(
        range(1, limit + 1),
        desc="a",
        unit="a",
        leave=False,
    ):
        for b in range(1, limit + 1):
            g_ab = gcd_table[a][b]
            for c in range(1, limit + 1):
                ac_sum = a + c
                g_bc = gcd_table[b][c]
                for d in range(1, limit + 1):
                    rectangle = ac_sum * (b + d)
                    g_cd = gcd_table[c][d]
                    g_ad = gcd_table[a][d]
                    boundary = g_ab + g_bc + g_ad + g_cd
                    interior = (rectangle - boundary) // 2 + 1
                    if is_square[interior]:
                        total += 1
    return total


def count_quadrilaterals_pure_python_parallel(
    limit,
    is_square,
    gcd_table,
    cpu_count,
):
    chunks = []
    chunk_size = max(1, (limit + cpu_count - 1) // cpu_count)
    a_start = 1
    while a_start <= limit:
        a_end = min(limit + 1, a_start + chunk_size)
        chunks.append((limit, a_start, a_end, is_square, gcd_table))
        a_start = a_end
    total = 0
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        for partial in tqdm(
            executor.map(pure_python_worker, chunks),
            total=len(chunks),
            desc="chunks",
            unit="chunk",
            leave=False,
        ):
            total += partial
    return total


def count_quadrilaterals_pure_python(limit, is_square, gcd_table):
    cpu_count = os.cpu_count() or 1
    if cpu_count < 2 or limit <= 10:
        return count_quadrilaterals_pure_python_sequential(
            limit,
            is_square,
            gcd_table,
        )
    return count_quadrilaterals_pure_python_parallel(
        limit,
        is_square,
        gcd_table,
        cpu_count,
    )


def main():
    """
    Purpose
    -------
    Solve Project Euler problem 504, "Square on the Inside", for m = 100.

    Method / Math Rationale
    ----------------------
    Uses Pick's theorem A = i + b/2 - 1 for lattice polygons with integer vertices, where A
    is the area, i is the number of interior lattice points and b is the number of boundary
    lattice points. For quadrilateral ABCD with vertices (a, 0), (0, b), (-c, 0), (0, -d) and
    1 <= a, b, c, d <= m, the area is A = (a + c)(b + d) / 2 and the number of boundary
    points is b = gcd(a, b) + gcd(b, c) + gcd(c, d) + gcd(a, d). Hence the number of
    interior points is
        i(a, b, c, d) =
            ((a + c) * (b + d) - (gcd(a, b) + gcd(b, c) + gcd(c, d) + gcd(a, d))) // 2 + 1.
    The program precomputes a table of gcd values and evaluates i on a 100 x 100 grid of
    (c, d) pairs for each fixed (a, b) using vectorised NumPy operations. A boolean lookup
    table flags which integers up to the maximum possible interior count are perfect squares,
    so counting quadrilaterals reduces to testing i(a, b, c, d) against this table. The most
    expensive loop over a is wrapped by tqdm to expose progress. If NumPy is not available
    the code falls back to a pure-Python implementation that parallelises over a with
    ProcessPoolExecutor.

    Complexity
    ----------
    Let m be the upper bound on a, b, c and d. The vectorised algorithm performs Θ(m^4)
    arithmetic operations overall but keeps the inner two dimensions in compiled NumPy
    code, resulting in practical runtimes for m = 100. It requires Θ(m^2) additional memory
    for the gcd and helper grids. The pure-Python fallback also has Θ(m^4) time complexity
    but parallelises over all available CPU cores.

    References
    Project Euler problem 504, "Square on the Inside":
    https://projecteuler.net/problem=504
    Pick's theorem:
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    limit = 100
    max_interior = 2 * limit * limit
    use_numpy = np is not None
    is_square = build_square_lookup(max_interior, use_numpy=use_numpy)
    if use_numpy:
        result = count_quadrilaterals_vectorized(limit, is_square)
    else:
        gcd_table = precompute_gcd_table_python(limit)
        result = count_quadrilaterals_pure_python(limit, is_square, gcd_table)
    print(result)


if __name__ == "__main__":
    main()
