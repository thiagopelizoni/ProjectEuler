# Problem: https://projecteuler.net/problem=64
def fraction_sequence(limit):
    sequence = [2]
    k = 1
    while len(sequence) < limit:
        sequence.extend([1, 2 * k, 1])
        k += 1
    return sequence[:limit]

def convergence(sequence):
    numerator = 1
    denominator = sequence[-1]

    for term in sequence[-2:0:-1]:
        numerator, denominator = denominator, term * denominator + numerator

    numerator += sequence[0] * denominator

    return numerator, denominator

if __name__ == "__main__":
    sequence = fraction_sequence(100)
    numerator, denominator = convergence(sequence)

    numerator_sum = sum(map(int, str(numerator)))

    print(numerator_sum)
