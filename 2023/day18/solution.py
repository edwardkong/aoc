import os

def hex_map(line):
    hex_dirs = {'2': 'L', '0': 'R', '3': 'U', '1': 'D'}
    hex = line.split()[2][2:-1]
    return hex_dirs[hex[-1]], int(hex[:-1], 16)

def shoelace(edges):
    """Shoelace formula and Pick's theorem"""
    dirs = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
    area = perimeter = x = y = 0
    for dir, mag in edges:
        px, py = x, y
        x, y = (p + d * int(mag) for p, d in zip((x, y), dirs[dir]))
        perimeter += int(mag)
        area += (y * px - x * py)
    return perimeter + (abs(area) / 2 - perimeter / 2 + 1)

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()

    print(shoelace([line.split()[:2] for line in lines]))
    print(shoelace([hex_map(line) for line in lines]))