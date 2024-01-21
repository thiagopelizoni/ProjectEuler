# Problem: https://projecteuler.net/problem=72
def count_fractions(max_d):
    phi = list(range(max_d + 1))

    # Count the number of reduced proper fractions for each denominator using the sieve of Eratosthenes
    for i in range(2, max_d + 1):
        if phi[i] == i:
            for j in range(i, max_d + 1, i):
                phi[j] = phi[j] // i * (i - 1)

      # Subtract 1 to exclude the fraction 0/1
    return sum(phi) - 1

if __name__ == "__main__":
    limit = 1_000_000
    print(count_fractions(limit))
