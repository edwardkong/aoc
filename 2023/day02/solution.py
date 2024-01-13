import os
import re
from functools import reduce

def play_game(text: str):
    limit = {'red': 12, 'green': 13, 'blue': 14}
    rounds = re.split(r'[;:]', text)
    for round in rounds[1:]:
        if any(int(num) > limit[color] 
            for num, color in (cube.split()
                for cube in round.split(','))):
                    return 0

    game_num = int(rounds[0].split(' ')[1])
    return game_num

def optimize_game(text: str):
    min_limit = {'red': 0, 'green': 0, 'blue': 0}
    rounds = re.split(r'[;:]', text)
    for round in rounds[1:]:
        cubes = round.split(',')
        for num, color in (cube.split() for cube in cubes):
            min_limit[color] = max(min_limit[color], int(num))

    power_cube = reduce(lambda x, y: x * y, min_limit.values())
    return power_cube

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    day = 2
    lines = process_input()

    print(sum(play_game(line) for line in lines))
    print(sum(optimize_game(line) for line in lines))