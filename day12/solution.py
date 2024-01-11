import re
from functools import cache

def spring_unpacker(line: str, unfold=False):
    springs, *groups = re.split(' |,', line)
    if not unfold:
        springs = f'{springs}.'
        groups = tuple(int(x) for x in groups)
    else:
        springs = '?'.join([springs] * 5) + '.'
        groups = tuple(int(x) for x in groups) * 5
    return springs, groups

@cache
def count_arrangements(springs, groups, curr_group=0):
    if not springs:
        return not groups and not curr_group
    res = 0
    s = springs[0]
    if s == '?' or s == '#':
        res += count_arrangements(springs[1:], groups, curr_group + 1)
    if s == '?' or s == '.':
        if curr_group:
            if groups and groups[0] == curr_group:
                res += count_arrangements(springs[1:], groups[1:])
        else:
            res += count_arrangements(springs[1:], groups)
    return res

def main_part_one():
    r_sum = 0
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            springs, groups = spring_unpacker(line.strip())
            r_sum += count_arrangements(springs, groups)
    return r_sum

def main_part_two():
    r_sum = 0    
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            springs, groups = spring_unpacker(line.strip(), unfold=True)
            r_sum += count_arrangements(springs, groups)
    return r_sum

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())