# Problem: https://projecteuler.net/problem=33
from fractions import Fraction

def main():
    product = 1

    for numerator in range(10, 100):
        for denominator in range(numerator + 1, 100):
            num_digits = [int(digit) for digit in str(numerator)]
            den_digits = [int(digit) for digit in str(denominator)]

            common_digits = list(set(num_digits) & set(den_digits))

            if common_digits and common_digits[0] != 0:
                num_digits.remove(common_digits[0])
                den_digits.remove(common_digits[0])

                if den_digits[0] != 0:
                    simplified_numerator   = num_digits[0]
                    simplified_denominator = den_digits[0]

                    if numerator / denominator == simplified_numerator / simplified_denominator:
                        product *= Fraction(numerator, denominator)

    result = product.denominator
    print(result)

if __name__ == "__main__":
    main()
