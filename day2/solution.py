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
            
def main_part_one():
    r_sum = 0
    with open('day2/input.txt', 'r') as file:
        for line in file:
            r_sum += play_game(line)
    return r_sum

def main_part_two():
    r_sum = 0
    with open('day2/input.txt', 'r') as file:
        for line in file:
            r_sum += optimize_game(line)
    return r_sum

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())