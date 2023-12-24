import re

NUMS = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
}

def intify(value: str) -> int:
    return int(NUMS[value]) if value in NUMS else int(value)

def digit_sandwich(text: str) -> int:
    pattern = r'^.*?(\d)(?:.*?(\d))?[^\d]*$'
    match = re.search(pattern, text)

    first = int(match.group(1))
    last = int(match.group(2)) if match.group(2) else first
    
    return first * 10 + last

def num_sandwich(text: str) -> int:
    pattern = rf"{'|'.join(list(NUMS.keys()) + ['\\d'])}"
    matches = re.findall(pattern, text)

    for match in matches:
        new_match = f"{intify(match)}{match[-1]}"
        text = re.sub(match, new_match, text)

    matches = re.findall(pattern, text)
    first = intify(matches[0])
    last = intify(matches[-1])

    return first * 10 + last

def main():
    r_sum = 0
    with open('day1/input.txt', 'r') as file:
        for line in file:
            r_sum += num_sandwich(line)
    return r_sum

if __name__ == '__main__':
    print(main())