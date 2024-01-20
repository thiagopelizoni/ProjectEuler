# Problem: https://projecteuler.net/problem=42
import requests

def is_triangle_number(n):
    """Check if a number is a triangle number."""
    x = (8 * n + 1)**0.5
    return x.is_integer()

# Redefine the function to calculate the alphabetical value of a word
def word_value(word):
    """Calculate the alphabetical value of a word."""
    return sum(ord(char) - 64 for char in word)

def words():
    url = "https://projecteuler.net/resources/documents/0042_words.txt"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error to fetch {url}")

    return response.content.decode('utf-8').replace('"', '').split(',')

def main():
    word_list = words()

    triangle_words_count = sum(is_triangle_number(word_value(word)) for word in word_list)

    print(triangle_words_count)

if __name__ == "__main__":
    main()
