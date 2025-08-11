# Problem: https://projecteuler.net/problem=140
from gmpy2 import mpz, mpfr, get_context, sqrt, floor


def generate_sequence_values(total_terms):
    starting_values = [mpz(7), mpz(14), mpz(50), mpz(97)]
    sequence_values = starting_values.copy()

    for _ in range(total_terms - 4):
        next_value = 7 * sequence_values[-2] - sequence_values[-4]
        sequence_values.append(next_value)

    return sequence_values


def sum_of_first_nuggets(total_nuggets):
    get_context().precision = 256

    sqrt_five = sqrt(mpfr(5))
    sequence_values = generate_sequence_values(total_nuggets)

    nugget_values = []

    for sequence_value in sequence_values:
        ratio_value = mpfr(sequence_value) / sqrt_five
        nugget_value = int(floor(ratio_value)) - 1
        nugget_values.append(nugget_value)

    return sum(nugget_values)


def main():
    total_nuggets = 30
    result = sum_of_first_nuggets(total_nuggets)
    print(result)


if __name__ == "__main__":
    main()
