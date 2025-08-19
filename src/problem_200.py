# Problem: https://projecteuler.net/problem=200
import gmpy2
from gmpy2 import mpz, is_prime, next_prime
import heapq
from tqdm import tqdm
import math

class SqubeGenerator:
    def __init__(self, exponent_small, exponent_large):
        self.exponent_small = exponent_small
        self.exponent_large = exponent_large
        self.priority_queue = []
        self.current_maximum_small_prime = 2
        self.next_small_prime = next_prime(2)
        initial_large_prime = next_prime(2)
        initial_value = pow(mpz(2), exponent_small) * pow(mpz(initial_large_prime), exponent_large)
        heapq.heappush(self.priority_queue, (initial_value, 2, initial_large_prime))

    def get_next_sqube(self):
        value, small_prime, large_prime = heapq.heappop(self.priority_queue)
        next_large = next_prime(large_prime)
        new_value = pow(mpz(small_prime), self.exponent_small) * pow(mpz(next_large), self.exponent_large)
        heapq.heappush(self.priority_queue, (new_value, small_prime, next_large))
        if small_prime == self.current_maximum_small_prime:
            new_small_prime = self.next_small_prime
            new_large_prime = next_prime(new_small_prime)
            new_value = pow(mpz(new_small_prime), self.exponent_small) * pow(mpz(new_large_prime), self.exponent_large)
            heapq.heappush(self.priority_queue, (new_value, new_small_prime, new_large_prime))
            self.current_maximum_small_prime = new_small_prime
            self.next_small_prime = next_prime(new_small_prime)
        return value

def has_substring_200(digits_list):
    digits_length = len(digits_list)
    for index in range(digits_length - 2):
        if digits_list[index] == 2 and digits_list[index + 1] == 0 and digits_list[index + 2] == 0:
            return True
    return False

def is_prime_proof(number):
    if number <= 1:
        return True
    digits_list = []
    temp_number = mpz(number)
    while temp_number > 0:
        digits_list.append(int(temp_number % 10))
        temp_number = temp_number // 10
    digits_list.reverse()
    digits_length = len(digits_list)
    is_even_number = digits_list[-1] % 2 == 0
    positions_to_check = [digits_length - 1] if is_even_number else range(digits_length)
    for position in positions_to_check:
        original_digit = digits_list[position]
        power_value = pow(mpz(10), digits_length - 1 - position)
        start_digit = 1 if position == 0 else 0
        for new_digit in range(start_digit, 10):
            if new_digit == original_digit:
                continue
            if position == digits_length - 1 and new_digit % 2 == 0:
                continue
            modified_number = number + (new_digit - original_digit) * power_value
            if is_prime(modified_number):
                return False
    return True

def find_200th_prime_proof_sqube():
    generator_a = SqubeGenerator(3, 2)
    generator_b = SqubeGenerator(2, 3)
    found_count = 0
    processed_count = 0
    update_interval = 10000
    progress_bar = tqdm(desc="Processing squbes")
    while True:
        current_a = generator_a.priority_queue[0][0] if generator_a.priority_queue else math.inf
        current_b = generator_b.priority_queue[0][0] if generator_b.priority_queue else math.inf
        if current_a <= current_b:
            current_value = generator_a.get_next_sqube()
        else:
            current_value = generator_b.get_next_sqube()
        processed_count += 1
        if processed_count % update_interval == 0:
            progress_bar.update(update_interval)
        digits_list = []
        temp_number = current_value
        while temp_number > 0:
            digits_list.append(int(temp_number % 10))
            temp_number = temp_number // 10
        digits_list.reverse()
        if has_substring_200(digits_list):
            if is_prime_proof(current_value):
                found_count += 1
                if found_count == 200:
                    progress_bar.update(processed_count % update_interval)
                    progress_bar.close()
                    return current_value

if __name__ == "__main__":
    result = find_200th_prime_proof_sqube()
    print(result)