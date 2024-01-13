import os
from functools import cache

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

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        s, g = zip(*[line.split() for line in file.read().splitlines()])
        spr = [f'{spring}.' for spring in s]
        grp = [tuple(map(int, group.split(','))) for group in g]
        wide_s = ['?'.join([x] * 5) + '.' for x in s]
        wide_g = [group * 5 for group in grp]
        return spr, grp, wide_s, wide_g

if __name__ == '__main__':
    spr, grp, wide_spr, wide_grp = process_input()
    print(sum(count_arrangements(s, g) for s, g in zip(spr, grp)))
    print(sum(count_arrangements(s, g) for s, g in zip(wide_spr, wide_grp)))