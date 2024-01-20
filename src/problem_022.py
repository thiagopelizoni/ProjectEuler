# Problem: https://projecteuler.net/problem=22
import requests

def get_names():
    url = "https://projecteuler.net/resources/documents/0022_names.txt"

    response = requests.get(url)

    if response.status_code == 200:
        return response.text.replace('"', '').split(',')
    else:
        raise Exception(f"Erro ao acessar a URL: {response.status_code}")

def calculate_name_score(names):
    names = sorted(names)
    total_score = 0

    for i, name in enumerate(names):
        name_score     = sum(ord(char) - ord('A') + 1 for char in name)
        weighted_score = (i + 1) * name_score
        total_score   += weighted_score

    return total_score

def main():
    names = get_names()
    total_score = calculate_name_score(names)
    print(total_score)

if __name__ == "__main__":
    main()
