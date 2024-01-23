# Problem: https://projecteuler.net/problem=98
import itertools
import requests

def get_words():
    # URL do arquivo TXT
    url = "https://projecteuler.net/resources/documents/0098_words.txt"

    # Fazer uma solicitação GET para baixar o arquivo
    response = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}")

    # Decodificar o conteúdo do arquivo como texto
    words = response.text

    word_list = [word.strip('"') for word in words.split(',')]

    return word_list

# Function to determine if two words are anagrams
def are_anagrams(word1, word2):
    return sorted(word1) == sorted(word2)

# Function to determine if a number is a perfect square
def is_square(n):
    return int(n**0.5) ** 2 == n

# Function to generate all possible digit assignments for a word
def get_digit_mappings(word):
    unique_letters = ''.join(set(word))
    for digits in itertools.permutations('1234567890', len(unique_letters)):
        table = str.maketrans(unique_letters, ''.join(digits))
        yield word.translate(table)

def main():
    # Find all square anagram word pairs
    square_anagram_pairs = []
    squares = set()

    words = get_words()
    # Generate squares up to the maximum possible based on the longest word length
    max_word_length = max(len(word) for word in words)
    max_square = int('9' * max_word_length)  # largest possible number with max_word_length digits
    n = 1
    while True:
        square = n * n
        if square > max_square:
            break
        squares.add(str(square))
        n += 1

    # Iterate through all pairs of words to find anagrams
    for word1, word2 in itertools.combinations(words, 2):
        if are_anagrams(word1, word2):
            # Check if any digit assignment makes both words squares
            for digit_mapping in get_digit_mappings(word1):
                if digit_mapping[0] != '0' and digit_mapping in squares:
                    square_word2 = word2.translate(str.maketrans(word1, digit_mapping))
                    if square_word2 in squares:
                        square_anagram_pairs.append((int(digit_mapping), int(square_word2)))

    # Sort the list by the maximum square in each pair and get the largest square
    largest_square = max(max(pair) for pair in square_anagram_pairs)
    print(largest_square)

if __name__ == "__main__":
    main()
