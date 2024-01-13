import os
import re

NUMS = {
    'one': 1, 'two': 2, 'three': 3, 
    'four': 4, 'five': 5, 'six': 6, 
    'seven': 7, 'eight': 8, 'nine': 9
}

def word_to_int(value: str) -> int:
    return int(NUMS[value]) if value in NUMS else int(value)

def digit_sandwich(text: str) -> int:
    pattern = r'^.*?(\d)(?:.*?)(\d)?[^\d]*$'
    match = re.search(pattern, text)

    first = int(match.group(1))
    last = int(match.group(2)) if match.group(2) else first
    
    return first * 10 + last

def num_sandwich(text: str) -> int:
    pattern = r'|'.join(list(NUMS.keys()) + ['\\d'])
    matches = re.findall(pattern, text)

    for match in matches:
        new_match = f"{word_to_int(match)}{match[-1]}"
        text = re.sub(match, new_match, text)

    matches = re.findall(pattern, text)

    first = word_to_int(matches[0])
    last = word_to_int(matches[-1])

    return first * 10 + last

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()

    print(sum(digit_sandwich(line) for line in lines))
    print(sum(num_sandwich(line) for line in lines))