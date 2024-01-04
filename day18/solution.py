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

def main_part_one():
    with open('day18/input.txt', 'r') as file:
        lines = [line.split()[:2] for line in file.read().splitlines()]
    return shoelace(lines)

def main_part_two():    
    with open('day18/input.txt', 'r') as file:
        lines = [hex_map(line) for line in file.read().splitlines()]
    return shoelace(lines)

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())