# Problem: https://projecteuler.net/problem=75
from math import gcd
from collections import Counter

max_limit = 1_500_000

triangles_count_per_length = Counter()

# Gerar triângulos pitagóricos usando a fórmula de Euclides
for m in range(2, int((max_limit / 2)**0.5) + 1):
    for n in range(1, m):
        if (m - n) % 2 == 1 and gcd(m, n) == 1:
            side_a = m**2 - n**2
            side_b = 2 * m * n
            side_c = m**2 + n**2
            perimeter = side_a + side_b + side_c
            if perimeter <= max_limit:
                for k in range(1, max_limit // perimeter + 1):
                    triangles_count_per_length[k * perimeter] += 1

# Contar o número de comprimentos com exatamente um triângulo
singular_triangle_lengths = sum(1 for count in triangles_count_per_length.values() if count == 1)
print(singular_triangle_lengths)
