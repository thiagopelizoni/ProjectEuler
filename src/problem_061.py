# Problem: https://projecteuler.net/problem=61

def poly_number(s, n):
    if s == 3:
        return n * (n + 1) // 2
    if s == 4:
        return n * n
    if s == 5:
        return n * (3 * n - 1) // 2
    if s == 6:
        return n * (2 * n - 1)
    if s == 7:
        return n * (5 * n - 3) // 2
    if s == 8:
        return n * (3 * n - 2)

# Find cycles
def find_cycles(poly_nums, sequence=[]):
    if len(sequence) == 6:  # If the sequence has 6 numbers, we check if it's cyclic
        if str(sequence[-1])[2:] == str(sequence[0])[:2]:
            return sequence
        return None

    if not sequence:  # If the sequence is empty, we try to start with numbers from any polygonal type
        for s, numbers in poly_nums.items():
            for number in numbers:
                result = find_cycles({k: v for k, v in poly_nums.items() if k != s}, sequence + [number])
                if result:
                    return result
    else:
        last_two_digits = str(sequence[-1])[2:]  # Get the last two digits of the last number in the sequence
        for s, numbers in poly_nums.items():
            if s not in [seq % 100 for seq in sequence]:  # Ensure we use each polygonal type exactly once
                for number in numbers:
                    if str(number)[:2] == last_two_digits:  # Check if the first two digits match
                        result = find_cycles({k: v for k, v in poly_nums.items() if k != s}, sequence + [number])
                        if result:
                            return result
    return None

if __name__ == "__main__":
    poly_numbers = {s: [poly_number(s, n) for n in range(20, 150) if 1000 <= poly_number(s, n) <= 9999] for s in range(3, 9)}
    cyclic_sequence = find_cycles(poly_numbers)
    answer = sum(cyclic_sequence) if cyclic_sequence else None
    print(answer)
