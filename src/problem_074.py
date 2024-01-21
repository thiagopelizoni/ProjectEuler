from math import factorial

def sum_factorial_digits(n):
    return sum(factorial(int(digit)) for digit in str(n))

factorial_digit_sum = {i: sum_factorial_digits(i) for i in range(10)}

# Define a function to find the next number in the chain
def next_number(n):
    return sum(factorial_digit_sum[int(digit)] for digit in str(n))

def digit_factorial_chains(limit):
    chains_with_60_terms = 0
    chain_length = {}

    for start in range(1, limit):
        n = start
        chain = []

        while n not in chain and n not in chain_length:
            chain.append(n)
            n = next_number(n)

        if n in chain_length:
            length = len(chain) + chain_length[n]
        else:
            length = len(chain)

        chain_length[start] = length

        if length == 60:
            chains_with_60_terms += 1

    return chains_with_60_terms

if __name__ == "__main__":
    limit = 1_000_000
    print(digit_factorial_chains(limit))
