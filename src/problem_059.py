# Problem: https://projecteuler.net/problem=59
import requests
from itertools import cycle, product

def get_encrypted_message():
    url = 'https://projecteuler.net/project/resources/p059_cipher.txt'
    response = requests.get(url)
    return list(map(int, response.text.strip().split(',')))

def decrypt_message(encrypted_message, key):
    return ''.join(chr(c ^ k) for c, k in zip(encrypted_message, cycle(key)))

def find_key_and_decrypt(encrypted_message):
    for key in product(range(97, 123), repeat=3):
        decrypted = decrypt_message(encrypted_message, key)
        if ' the ' in decrypted:
            return decrypted, key

if __name__ == "__main__":
    encrypted_message = get_encrypted_message()
    decrypted_message, key = find_key_and_decrypt(encrypted_message)
    answer = sum(ord(c) for c in decrypted_message)
    print(answer)
