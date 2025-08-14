# Problem: https://projecteuler.net/problem=168
from tqdm import tqdm

MOD = 100000
total_sum_last_five = 0

for digits in tqdm(range(2, 101)):
    ten_to_digits = 10 ** digits
    repunit_like = ten_to_digits - 1

    for multiplier in range(1, 10):
        denominator = 10 * multiplier - 1

        for last_digit in range(1, 10):
            product = last_digit * repunit_like

            if product % denominator == 0:
                number = product // denominator

                number_str = str(number)
                if len(number_str) == digits and number > 10:
                    total_sum_last_five = (total_sum_last_five + (number % MOD)) % MOD

print(total_sum_last_five)