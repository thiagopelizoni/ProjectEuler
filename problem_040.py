# Problem: https://projecteuler.net/problem=40
def champernowne_constant():
    index_product = 1
    current_number = 1
    current_index = 1
    desired_indices = [1, 10, 100, 1000, 10000, 100000, 1000000]

    while desired_indices:
        number_str = str(current_number)
        for digit in number_str:
            if current_index in desired_indices:
                index_product *= int(digit)
                desired_indices.remove(current_index)
            current_index += 1
        current_number += 1

    return index_product

answer = champernowne_constant()
print(answer)
