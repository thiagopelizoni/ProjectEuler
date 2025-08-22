# Problem: https://projecteuler.net/problem=230
from tqdm import tqdm

first_string = '1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679'
second_string = '8214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196'

max_word_index = 200
word_lengths = [0] * (max_word_index + 1)
word_lengths[1] = len(first_string)
word_lengths[2] = len(second_string)
for current_index in range(3, max_word_index + 1):
    word_lengths[current_index] = word_lengths[current_index - 1] + word_lengths[current_index - 2]

def find_smallest_word_index_for_position(global_position):
    current_word_index = 1
    while word_lengths[current_word_index] < global_position:
        current_word_index += 1
    return current_word_index

def get_digit_at_position(word_index, position):
    current_word_index = word_index
    current_position = position
    while current_word_index > 2:
        length_of_earlier_word = word_lengths[current_word_index - 2]
        if current_position > length_of_earlier_word:
            current_position -= length_of_earlier_word
            current_word_index -= 1
        else:
            current_word_index -= 2
    if current_word_index == 1:
        return int(first_string[current_position - 1])
    else:
        return int(second_string[current_position - 1])

final_result = 0
for current_n in tqdm(range(18)):
    current_exponent = 7 ** current_n
    current_multiplier = 127 + 19 * current_n
    global_position = current_multiplier * current_exponent
    suitable_word_index = find_smallest_word_index_for_position(global_position)
    current_digit = get_digit_at_position(suitable_word_index, global_position)
    final_result += current_digit * (10 ** current_n)

print(final_result)