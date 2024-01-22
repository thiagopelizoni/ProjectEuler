# Problem: https://projecteuler.net/problem=89
import requests

def fetch_roman_numerals():
    url = "https://projecteuler.net/resources/documents/0089_roman.txt"

    response = requests.get(url)
    file_lines = response.text.strip().split('\n')

    roman_numerals = []
    for line in file_lines:
        roman_numerals.append(str(line))
    return roman_numerals

def roman_to_int(roman):

    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    num = 0

    for i in range(len(roman)):
        if i == len(roman) - 1 or roman_dict[roman[i]] >= roman_dict[roman[i + 1]]:
            num += roman_dict[roman[i]]

        else:
            num -= roman_dict[roman[i]]
    return num

def int_to_min_roman(num):
    numeral_map = zip(
        [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1],
        ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    )
    result = ""
    for i, numeral in numeral_map:
        while num >= i:
            result += numeral
            num -= i
    return result

total_saved = 0
roman_numerals = fetch_roman_numerals()

for roman in roman_numerals:
    num = roman_to_int(roman)
    minimal_roman = int_to_min_roman(num)
    saved = len(roman) - len(minimal_roman)
    total_saved += saved

print(total_saved)
