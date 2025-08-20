# Problem: https://projecteuler.net/problem=206
import math
import multiprocessing
from tqdm import tqdm

min_squared_number = 1020304050607080900
max_squared_number = 1929394959697989990

min_n_value = int(math.sqrt(min_squared_number)) + 1
while min_n_value ** 2 < min_squared_number:
    min_n_value += 1

max_n_value = int(math.sqrt(max_squared_number))
while (max_n_value + 1) ** 2 <= max_squared_number:
    max_n_value += 1

possible_residues_list = [i for i in range(1000) if (i * i) % 1000 == 900]

def check_for_residue(modulo_residue):
    residue_start_n = min_n_value + (modulo_residue - min_n_value % 1000) % 1000
    if residue_start_n < min_n_value:
        residue_start_n += 1000
    current_n_value = residue_start_n
    while current_n_value <= max_n_value:
        square_of_n = current_n_value * current_n_value
        string_of_square = str(square_of_n)
        if (string_of_square[0] == '1' and
            string_of_square[2] == '2' and
            string_of_square[4] == '3' and
            string_of_square[6] == '4' and
            string_of_square[8] == '5' and
            string_of_square[10] == '6' and
            string_of_square[12] == '7' and
            string_of_square[14] == '8' and
            string_of_square[16] == '9' and
            string_of_square[18] == '0'):
            return current_n_value
        current_n_value += 1000
    return None

if __name__ == '__main__':
    with multiprocessing.Pool() as processing_pool:
        results = list(tqdm(
            processing_pool.imap(check_for_residue, possible_residues_list),
            total=len(possible_residues_list),
            desc="Processing residues"
        ))
    found_number = next(r for r in results if r is not None)
    print(found_number)