# Problem: https://projecteuler.net/problem=97

multiplier = 28_433
power_of_two = 7_830_457
modulus = 10**10

# Calculate 2^7830457 mod 10^10 using efficient exponentiation
last_ten_digits = pow(2, power_of_two, modulus)

# Multiply by 28433 and add 1, then take mod 10^10 again to find the last ten digits
last_ten_digits = (last_ten_digits * multiplier + 1) % modulus

print(last_ten_digits)
