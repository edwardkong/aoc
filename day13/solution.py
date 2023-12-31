def find_reflection(pattern: list[str], fix=False) -> int:
    if (row:= mirror_row(pattern, fix)) is not None:
        return 100 * (row + 1)
    r_pat = list(map(''.join, zip(*reversed(pattern))))
    if (col:= mirror_row(r_pat, fix)) is not None:
        return col + 1
    return 0

def mirror_row(pattern: list[str], fix=False) -> int:
    n_rows = len(pattern)
    for row in range(n_rows - 1):
        if not fix and pattern[row] == pattern[row + 1] or fix:
            mir = min(row, n_rows - row - 2)
            l, r = pattern[row - mir:row + 1], pattern[row + mir + 1:row:-1]
            if not fix and l == r or fix and compare_mirrors(l, r) == 1:
                return row
    return None

def compare_mirrors(left: list[str], right: list[str]):
    one_diff = False
    for l, r in zip(''.join(left), ''.join(right)):
        if l != r:
            if one_diff:
                return False
            one_diff = True
    return one_diff

def main_part_one():
    r_sum = 0
    with open('day13/input.txt', 'r') as file:
        for pattern in file.read().split('\n\n'):
            r_sum += find_reflection(pattern.split('\n'))
    return r_sum

def main_part_two():
    r_sum = 0    
    with open('day13/input.txt', 'r') as file:
        for pattern in file.read().split('\n\n'):
            r_sum += find_reflection(pattern.split('\n'), fix=True)
    return r_sum

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())