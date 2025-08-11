from sympy import primerange
from gmpy2 import mpz


best_number = None


def depth_first_search(prime_list, prime_index, previous_exponent, current_number, current_divisors, required_divisors):
    global best_number

    if current_divisors > required_divisors:
        if best_number is None or current_number < best_number:
            best_number = current_number
        return

    if prime_index >= len(prime_list):
        return

    prime_value = mpz(prime_list[prime_index])
    temporary_number = mpz(current_number)

    for exponent in range(1, previous_exponent + 1):
        temporary_number *= prime_value

        if best_number is not None and temporary_number >= best_number:
            break

        new_divisors = current_divisors * (2 * exponent + 1)
        depth_first_search(
            prime_list,
            prime_index + 1,
            exponent,
            temporary_number,
            new_divisors,
            required_divisors,
        )


def minimal_n_with_solutions(target_solutions):
    global best_number

    required_divisors = 2 * target_solutions - 1
    prime_list = list(primerange(2, 100))
    best_number = None

    depth_first_search(
        prime_list=prime_list,
        prime_index=0,
        previous_exponent=64,
        current_number=mpz(1),
        current_divisors=1,
        required_divisors=required_divisors,
    )

    return int(best_number)


def main():
    target_solutions = 4_000_000
    result = minimal_n_with_solutions(target_solutions)
    print(result)


if __name__ == "__main__":
    main()
