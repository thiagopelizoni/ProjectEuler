def is_pandigital(s):
    return len(s) == 9 and not '0' in s and len(set(s)) == 9

def largest_pandigital_multiple():
    largest = 0
    limit = 10000

    for i in range(1, limit):
        concatenated_product = ''
        n = 1

        while len(concatenated_product) < 9:
            concatenated_product += str(i * n)
            n += 1

        if is_pandigital(concatenated_product):
            largest = max(largest, int(concatenated_product))

    return largest

largest_pandigital = largest_pandigital_multiple()
print(largest_pandigital)
