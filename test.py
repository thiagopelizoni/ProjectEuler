from sympy import primerange

# Function to calculate the number of ways to write a number as a sum of k terms
def count_ways(n, k, min_factor=2):
    ways = 0
    if k == 1:
        if n >= min_factor:
            return 1
        else:
            return 0
    for i in range(min_factor, int(n**0.5) + 1):
        if n % i == 0:
            ways += count_ways(n // i, k - 1, i)
    return ways

# Calculate the minimal product-sum for each k
def minimal_product_sums(k_max):
    k_values = [2 * k_max] * (k_max + 1)
    primes = list(primerange(1, k_max))
    for i in range(2, k_max * 2):
        for k in range(2, k_max + 1):
            if count_ways(i, k) > 0:
                k_values[k] = min(k_values[k], i)
    return set(k_values[2:])

# Find the sum of all the minimal product-sum numbers for 2 ≤ k ≤ 12000
k_limit = 12000
sum_of_minimal_product_sums = sum(minimal_product_sums(k_limit))
print(sum_of_minimal_product_sums)
