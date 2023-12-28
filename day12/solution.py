import re
from collections import deque
from itertools import product
import math

def spring_unpacker(line: str, unfold=False):
    springs, *groups = re.split(' |,', line)
    groups = [int(x) for x in groups]
    if unfold:
        springs = '?'.join(springs * 5)
        groups = groups * 5
    return springs, groups

def count_arrangements(line: str) -> int:
    def backtrack(index: int, line_builder: str):
        if index == len(springs):
            matches = re.findall(r'#+', line_builder)
            matches_lengths = [len(x) for x in matches]
            if matches_lengths == groups:
                p.add(line_builder)
            return
    
        if springs[index] == '?':
            backtrack(index + 1, line_builder + '#')
            backtrack(index + 1, line_builder + '.')
        else:
            backtrack(index + 1, line_builder + springs[index])

    springs, *groups = re.split(' |,', line)
    groups = [int(x) for x in groups]
    p = set()
    backtrack(0, '')
    return len(p)

    
    

def main_part_one():
    r_sum = 0
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            r_sum += count_arrangements(line.strip())
        return r_sum


def main_part_two():
    with open('day12/input.txt', 'r') as file:
        pass

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())