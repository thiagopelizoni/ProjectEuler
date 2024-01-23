# Problem: https://projecteuler.net/problem=99
import requests
import math

url = "https://projecteuler.net/resources/documents/0099_base_exp.txt"

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Failed to fetch {url}")

max_value = 0
max_line = 0
line_number = 0

lines = response.text.split("\n")

for line in lines:
    line_number += 1
    base, exponent = map(int, line.strip().split(','))

    # Calculate the value of the exponent for comparison using logarithms to avoid large numbers
    current_value = exponent * math.log(base)

    if current_value > max_value:
        max_value = current_value
        max_line = line_number

print(max_line)
