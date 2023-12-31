import re
from functools import cache

def spring_unpacker(line: str, unfold=False):
    springs, *groups = re.split(' |,', line)
    if not unfold:
        springs = [x for x in springs]
        groups = [int(x) for x in groups]
    else:
        springs = '?'.join([springs] * 5) + '.'
        groups = [int(x) for x in groups] * 5
    return springs, groups

def is_valid_springs(springs: str, groups: list[int], n_char: int) -> bool:
    if not groups:
        return False
    group = 0
    curr_block = 0
    for ch in springs:
        if ch == '#':
            if group == -1:
                return False
            curr_block += 1
            if curr_block > groups[group]:
                return False
            
        elif ch == '.':
            if curr_block > 0:
                if curr_block != groups[group]:
                    return False
                else:
                    if group == len(groups) - 1:
                        group = -1
                    elif group != -1:
                        group += 1
            curr_block = 0

    if curr_block > groups[group]:
        return False
    if n_char == len(springs):
        return ((curr_block == groups[group] and group == len(groups) - 1) or 
                (group == -1 and curr_block == 0))
    else:
        return curr_block == 0 or curr_block <= groups[group]


def count_arrangements(line: str, unfold=False) -> int:
    @cache
    def backtrack(index: int, line_builder: str):
        if not is_valid_springs(line_builder, groups, n):
            return 0
        if index == n:
            return 1
    
        if springs[index] == '?':
            result = (backtrack(index + 1, line_builder + '#') +
                      backtrack(index + 1, line_builder + '.'))
        else:
            result = backtrack(index + 1, line_builder + springs[index])
        return result

    springs, groups = spring_unpacker(line, unfold)
    n = len(springs)
    return backtrack(0, '')

@cache
def count_arrangements1(springs, groups, curr_group=0):
    if not springs:
        return not groups and not curr_group
    res = 0
    if springs[0] == '?':
        res += count_arrangements1(springs[1:], groups, curr_group + 1)
        if curr_group:
            if groups and groups[0] == curr_group:
                res += count_arrangements1(springs[1:], groups[1:])
        else:
            res += count_arrangements1(springs[1:], groups)
    else:
        if springs[0] == '#':
            res += count_arrangements1(springs[1:], groups, curr_group + 1)
        else:
            if curr_group:
                if groups and groups[0] == curr_group:
                    res += count_arrangements1(springs[1:], groups[1:])
            else:
                res += count_arrangements1(springs[1:], groups)
    return res

def main_part_one():
    r_sum = 0
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            r_sum += count_arrangements(line.strip())
        return r_sum

def main_part_two():
    r_sum = 0    
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            springs, groups = spring_unpacker(line.strip(), unfold=True)
            r_sum += count_arrangements1(springs, tuple(groups))
            #r_sum += count_arrangements(line, unfold=True)
    
        return r_sum

if __name__ == '__main__':
    #print(main_part_one())
    print(main_part_two())